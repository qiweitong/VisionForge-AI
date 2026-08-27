import sqlite3
from datetime import datetime
from pathlib import Path

project_root = Path(__file__).parent.parent
DB_NAME = project_root / "database" / "history.db"


def get_conn():
    conn = sqlite3.connect(str(DB_NAME))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    DB_NAME.parent.mkdir(parents=True, exist_ok=True)
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_name TEXT,
            class_name TEXT,
            class_cn TEXT,
            confidence REAL,
            inference_time REAL,
            model_name TEXT DEFAULT 'resnet',
            create_time TEXT DEFAULT (datetime('now','localtime'))
        )
    ''')

    cols = [row[1] for row in cursor.execute("PRAGMA table_info(history)").fetchall()]
    if "model_name" not in cols:
        cursor.execute("ALTER TABLE history ADD COLUMN model_name TEXT DEFAULT 'resnet'")

    conn.commit()
    conn.close()


def insert_history(image_name, class_name, class_cn, confidence, model_name="resnet"):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO history(
            image_name, class_name, class_cn, confidence, inference_time, model_name
        )
        VALUES(?,?,?,?,?,?)
    """, (image_name, class_name, class_cn, confidence, 0.0, model_name))
    conn.commit()
    record_id = cursor.lastrowid
    conn.close()
    return record_id


def get_history(limit=100, offset=0, model_name=None):
    conn = get_conn()
    cursor = conn.cursor()

    if model_name:
        cursor.execute("""
            SELECT * FROM history
            WHERE model_name = ?
            ORDER BY id DESC
            LIMIT ? OFFSET ?
        """, [model_name, limit, offset])
    else:
        cursor.execute("""
            SELECT * FROM history
            ORDER BY id DESC
            LIMIT ? OFFSET ?
        """, [limit, offset])

    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def delete_history(record_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history WHERE id = ?", [record_id])
    conn.commit()
    conn.close()


def clear_history(model_name=None):
    conn = get_conn()
    cursor = conn.cursor()
    if model_name:
        cursor.execute("DELETE FROM history WHERE model_name = ?", [model_name])
    else:
        cursor.execute("DELETE FROM history")
    conn.commit()
    conn.close()


def get_total_count(model_name=None):
    conn = get_conn()
    cursor = conn.cursor()
    if model_name:
        cursor.execute("SELECT COUNT(*) FROM history WHERE model_name = ?", [model_name])
    else:
        cursor.execute("SELECT COUNT(*) FROM history")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def get_class_distribution(limit=10, model_name=None):
    conn = get_conn()
    cursor = conn.cursor()
    if model_name:
        cursor.execute("""
            SELECT class_cn, COUNT(*) as count
            FROM history WHERE model_name = ?
            GROUP BY class_cn
            ORDER BY count DESC
            LIMIT ?
        """, [model_name, limit])
    else:
        cursor.execute("""
            SELECT class_cn, COUNT(*) as count
            FROM history
            GROUP BY class_cn
            ORDER BY count DESC
            LIMIT ?
        """, [limit])
    rows = cursor.fetchall()
    conn.close()
    return [(row["class_cn"], row["count"]) for row in rows]


def get_confidence_distribution(model_name=None):
    conn = get_conn()
    cursor = conn.cursor()
    if model_name:
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN confidence >= 0.9 THEN '0.9-1.0'
                    WHEN confidence >= 0.8 THEN '0.8-0.9'
                    WHEN confidence >= 0.7 THEN '0.7-0.8'
                    WHEN confidence >= 0.6 THEN '0.6-0.7'
                    ELSE '<0.6'
                END as range,
                COUNT(*) as count
            FROM history WHERE model_name = ?
            GROUP BY range
            ORDER BY range
        """, [model_name])
    else:
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN confidence >= 0.9 THEN '0.9-1.0'
                    WHEN confidence >= 0.8 THEN '0.8-0.9'
                    WHEN confidence >= 0.7 THEN '0.7-0.8'
                    WHEN confidence >= 0.6 THEN '0.6-0.7'
                    ELSE '<0.6'
                END as range,
                COUNT(*) as count
            FROM history
            GROUP BY range
            ORDER BY range
        """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_class_accuracy(model_name=None):
    conn = get_conn()
    cursor = conn.cursor()
    if model_name:
        cursor.execute("""
            SELECT class_cn, AVG(confidence) as accuracy
            FROM history WHERE model_name = ?
            GROUP BY class_cn
        """, [model_name])
    else:
        cursor.execute("""
            SELECT class_cn, AVG(confidence) as accuracy
            FROM history
            GROUP BY class_cn
        """)
    rows = cursor.fetchall()
    conn.close()
    return [{"class_cn": row["class_cn"], "accuracy": round(row["accuracy"] or 0, 4)} for row in rows]


def get_daily_trend(days=7, model_name=None):
    conn = get_conn()
    cursor = conn.cursor()
    if model_name:
        cursor.execute("""
            SELECT DATE(create_time) as date, COUNT(*) as count
            FROM history WHERE model_name = ?
            AND create_time >= DATE('now', ?)
            GROUP BY DATE(create_time)
            ORDER BY date
        """, [model_name, f"-{days} days"])
    else:
        cursor.execute("""
            SELECT DATE(create_time) as date, COUNT(*) as count
            FROM history
            WHERE create_time >= DATE('now', ?)
            GROUP BY DATE(create_time)
            ORDER BY date
        """, [f"-{days} days"])
    rows = cursor.fetchall()
    conn.close()
    return [(row["date"], row["count"]) for row in rows]


def get_statistics(model_name=None):
    conn = get_conn()
    cursor = conn.cursor()

    if model_name:
        base_where = "WHERE model_name = ?"
        params = [model_name]
    else:
        base_where = ""
        params = []

    cursor.execute(f"SELECT COUNT(*) FROM history {base_where}", params)
    total = cursor.fetchone()[0]

    today_str = datetime.now().strftime("%Y-%m-%d")
    if model_name:
        cursor.execute("""
            SELECT COUNT(*) FROM history
            WHERE DATE(create_time) = ? AND model_name = ?
        """, [today_str, model_name])
    else:
        cursor.execute("""
            SELECT COUNT(*) FROM history
            WHERE DATE(create_time) = ?
        """, [today_str])
    today = cursor.fetchone()[0]

    if model_name:
        cursor.execute("SELECT AVG(confidence) FROM history WHERE model_name = ?", [model_name])
    else:
        cursor.execute("SELECT AVG(confidence) FROM history")
    avg_confidence = cursor.fetchone()[0] or 0

    if model_name:
        cursor.execute("SELECT AVG(inference_time) FROM history WHERE model_name = ?", [model_name])
    else:
        cursor.execute("SELECT AVG(inference_time) FROM history")
    avg_time = cursor.fetchone()[0] or 0

    if model_name:
        cursor.execute("""
            SELECT class_cn, COUNT(*) as count
            FROM history WHERE model_name = ?
            GROUP BY class_cn
        """, [model_name])
    else:
        cursor.execute("""
            SELECT class_cn, COUNT(*) as count
            FROM history
            GROUP BY class_cn
        """)
    bar = cursor.fetchall()

    if model_name:
        cursor.execute("""
            SELECT class_cn, COUNT(*) as count
            FROM history WHERE model_name = ?
            GROUP BY class_cn
        """, [model_name])
    else:
        cursor.execute("""
            SELECT class_cn, COUNT(*) as count
            FROM history
            GROUP BY class_cn
        """)
    pie = cursor.fetchall()

    if model_name:
        cursor.execute("""
            SELECT DATE(create_time) as date, COUNT(*) as count
            FROM history WHERE model_name = ?
            GROUP BY DATE(create_time)
            ORDER BY DATE(create_time)
        """, [model_name])
    else:
        cursor.execute("""
            SELECT DATE(create_time) as date, COUNT(*) as count
            FROM history
            GROUP BY DATE(create_time)
            ORDER BY DATE(create_time)
        """)
    trend = cursor.fetchall()

    conn.close()

    return {
        "card": {
            "total": total,
            "today": today,
            "avgConfidence": round(avg_confidence * 100, 2),
            "avgTime": round(avg_time, 2)
        },
        "bar": [dict(i) for i in bar],
        "pie": [dict(i) for i in pie],
        "trend": [dict(i) for i in trend],
    }


if __name__ == "__main__":
    init_db()
    print("数据库初始化完成！")
