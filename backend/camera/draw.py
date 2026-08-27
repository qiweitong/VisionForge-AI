import cv2


def draw_info(frame, result, fps):
    cv2.rectangle(frame, (10, 10), (350, 180), (40, 40, 40), -1)

    if result:
        task_type = result.get("task_type", "unknown")

        if task_type == "classification":
            class_name = result.get("class_name", "N/A")
            confidence = result.get("confidence", 0)
            cv2.putText(
                frame,
                f"Class : {class_name}",
                (20, 45),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )
            cv2.putText(
                frame,
                f"Conf : {confidence * 100:.2f}%",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )
        elif task_type == "detection":
            detections = result.get("detections", [])
            count = len(detections)
            cv2.putText(
                frame,
                f"Detections : {count}",
                (20, 45),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )
            if detections:
                best = max(detections, key=lambda d: d["confidence"])
                cv2.putText(
                    frame,
                    f"Top : {best['class_name']} ({best['confidence'] * 100:.1f}%)",
                    (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

            for det in detections:
                bbox = det.get("bbox", [])
                if len(bbox) == 4:
                    x1, y1, x2, y2 = bbox
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    label = f"{det['class_name']} {det['confidence'] * 100:.1f}%"
                    cv2.putText(
                        frame,
                        label,
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 0, 255),
                        2
                    )

        model_type = task_type.upper()
        cv2.putText(
            frame,
            f"Model: {model_type}",
            (20, 115),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

    cv2.putText(
        frame,
        f"FPS : {fps:.1f}",
        (20, 155),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2
    )
