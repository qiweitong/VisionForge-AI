VisionForge AI｜工业缺陷视觉检测 + 机械臂具身闭环系统

> 一个面向工业质检场景的"视觉识别 → 决策 → 机械臂执行"完整具身智能闭环项目。
> 软件部分（视觉模型 / 后端服务 / 前端可视化 / Docker 部署 / ROS2 仿真 / 舵机 LLM 控制 / 语音模式）已全部跑通，机械臂硬件正在采购装配中。



一、项目简介

VisionForge AI 是一个工业钢材表面缺陷视觉检测系统，目标是把"视觉感知"和"机械臂执行"打通，构建一个完整的具身智能闭环：

1. 摄像头实时采集工件画面 → YOLO11 / ResNet50 推理检测缺陷
2. 检测结果上报后端服务 → 落库统计、前端可视化展示
3. 大模型 Agent 接收检测结果 → 决策动作 → 下发舵机角度指令
4. 总线舵机执行动作 → 完成从视觉到机械臂的闭环

项目设计了可扩展的多模型管理体系，未来新增 YOLOv12、RT-DETR 等模型只需实现 Predictor 接口并注册到 ModelManager，无需改动前后端业务代码。


二、技术栈

| 分层 | 技术选型 |
| --- | --- |
| 视觉模型 | PyTorch、ResNet50（图像分类）、YOLO11（目标检测，Ultralytics） |
| 后端服务 | FastAPI、Uvicorn、OpenCV、SQLite |
| 前端可视化 | Vue 3、Vite、Element Plus、ECharts 6、Vue Router |
| 实时推理 | OpenCV VideoCapture、MJPEG 流式推送、多线程帧抽取 |
| 部署运维 | Docker、Nginx 反向代理 |
| 机械臂 / 具身 | ROS2 七舵机机械臂仿真、总线舵机串口指令控制 |
| 大模型 Agent | LangChain / LangGraph、本地 LLM Agent，下发舵机角度指令 |
| 语音交互 | 语音模式（语音输入 → LLM 解析 → 舵机动作执行） |



三、已实现功能

1. 视觉模型层（model/）

基于 NEU-DET 钢材表面缺陷数据集，6 类缺陷：裂纹（Cr）、夹杂（In）、斑块（Pa）、点蚀（PS）、轧制氧化皮（RS）、划痕（Sc）。

ResNet50 分类模型（model/train.py、model/models/resnet.py）
基于 torchvision 预训练 ResNet18，替换 fc 层输出 6 类
Adam 优化器、CrossEntropyLoss、20 epoch、batch=32
训练保存最优权重到 model/output/weights/best.pth
model/evaluate.py 独立测试集评估脚本
YOLO11 目标检测模型(model/train_yolo.py、model/models/yolo.py）
基于 Ultralytics YOLO11n，配置 neu_det.yaml
40 epoch、imgsz=640、batch=4、patience=10、CPU 训练
输出 model/runs/yolo11n_steel/weights/best.pt
统一 Predictor 接口
ResNetPredictor / YOLOPredictor 均实现 predict() / predict_frame()
返回标准 Python dict（类别、置信度、bbox、推理耗时），不暴露 tensor / Ultralytics 对象
中英文类别映射（CLASS_CN_MAP），前端无需关心底层模型差异

2. 后端服务层（backend/）

按"API 层只处理请求响应，业务逻辑全部在 services 层"的工程约定组织。

入口backend/app.py：FastAPI 应用、CORS、路由聚合、启动初始化
统一模型管理 ModelManager（services/model_manager.py）
全局唯一模型入口，启动时加载 ResNet / YOLO 权重
提供 list_models / set_model / get_predictor / reload_yolo 等方法
硬约束：所有模型访问必须经 ModelManager，禁止直接 new Predictor
业务服务层
predict_service.py：单图推理 + 落库
camera_service.py：摄像头帧推理
history_service.py：历史记录查询 / 删除 / 清空
dashboard_service.py：统计看板数据
API 接口（api/）
POST /predict 单图上传检测（可在请求中切换模型）
GET /predict/list、DELETE /predict/{id}、DELETE /predict 历史管理
GET /video_feed MJPEG 实时视频流
POST /camera/start、POST /camera/stop、GET /camera/status 摄像头控制
GET /model/list、GET /model/curren、POST /model/select、POST /model/reload_yolo 模型管理
GET /history 历史记录、GET /statistics 统计看板
数据持久化（database/database.py）
SQLite 落库，history 表带 model_name字段区分不同模型数据
提供分类分布、置信度分布、准确率、每日趋势、看板汇总等多维统计 SQL
摄像头模块（camera/）
多线程 _read_loop 抽帧 + 帧跳（FRAME_SKIP=10）降推理压力
draw.py 在画面上叠加类别、置信度、检测框、FPS、当前模型
FPSCounter 实时帧率统计

3. 前端可视化层（frontend/）

Vue 3 + Vite + Element Plus + ECharts 单页应用。

页面路由（router/index.js）
Home 单图上传检测
Realtime 实时摄像头检测
History 检测历史记录表
Dashboard 数据统计看板
ModelManager 多模型管理
核心组件
UploadCard 图片选择 + 预览 + 触发检测
ResultCard 检测结果展示
DefectBarChart / DefectPieChart / TrendLineChart ECharts 图表
Header / Sidebar / MainLayout 整体布局
统一 API 层（api/）
   request.js axios 实例，统一 baseURL
   predict.js / model.js / history.js / statistics.js 分模块封装
   前端不直接引用具体模型（ResNet / YOLO），只通过统一接口交互
实时检测页
   MJPEG 流 + 200ms 轮询 `/camera/status` 刷新状态面板
   状态、模型、任务类型、类别、置信度、FPS 实时显示

4. 多模型可扩展架构

项目核心工程亮点：新增模型零业务改动。


新增模型步骤：
1. 在 model/models/ 下实现 Predictor 类（实现 predict / predict_frame）
2. 在 ModelManager.initialize() 中 register_model 注册
3. 前端自动出现在模型管理页，无需改动其他业务代码


POST /model/select 仅修改当前激活模型，所有后续推理走新模型；历史数据按 model_name 隔离。

5. 容器化部署（docker/）

后端 Dockerfile（docker/backend/Dockerfile）
python:3.11-slim 基础镜像
切清华 Debian 源、安装 OpenCV 依赖（libgl1 / libglib2.0）
单独装 CPU 版 PyTorch（--index-url https://download.pytorch.org/whl/cpu）
清华 pip 源安装项目依赖，EXPOSE 8000，CMD python app.py
Nginx 反向代理docker/nginx/nginx.conf
前端 Vite 构建产物 + Nginx 托管，统一对外服务

6. 机械臂具身单元（已实现）

ROS2 七舵机机械臂仿真环境：完成仿真搭建，可在仿真中验证运动学
总线舵机硬件调试
   已采购单总线舵机、调试板、锂电池
   通过串口指令下发角度，验证舵机转动
LLM Agent 下发舵机角度指令
   大模型直接输出舵机角度，经串口下发到舵机
    实现"自然语言 → 动作"链路
语音模式
    语音输入 → LLM 解析意图 → 下发舵机动作指令
    完成"语音 → 决策 → 执行"链路打通
待完成：剩余 6 个舵机采购到位后，完成实物七自由度机械臂整机联调，最终打通"视觉检测 → 实体机械臂执行"的完整具身闭环。


四、项目目录结构

VisionForge AI/
├── backend/                         # FastAPI 后端
│   ├── api/                         # 路由层（只处理请求响应）
│   │   ├── predict.py               # 单图检测 + 历史管理
│   │   ├── video.py                 # 实时视频流 + 摄像头控制
│   │   ├── model.py                 # 模型列表 / 切换 / 重载
│   │   ├── history.py               # 历史记录查询删除
│   │   └── statistics.py            # 统计看板
│   ├── services/                    # 业务逻辑层
│   │   ├── model_manager.py         # 统一模型管理入口
│   │   ├── predict_service.py
│   │   ├── camera_service.py
│   │   ├── history_service.py
│   │   └── dashboard_service.py
│   ├── camera/                      # 摄像头采集 + 推理 + 画面绘制
│   │   ├── camera.py                # 多线程抽帧
│   │   ├── draw.py                  # 结果叠加绘制
│   │   ├── fps.py                   # 帧率统计
│   │   └── config.py
│   ├── database/
│   │   └── database.py              # SQLite + 多维统计 SQL
│   ├── utils/
│   ├── app.py                       # FastAPI 入口
│   └── requirements.txt
├── frontend/                        # Vue 3 前端
│   └── src/
│       ├── api/                      # 统一 axios 接口封装
│       ├── components/               # 上传卡 / 结果卡 / 图表
│       ├── layouts/                  # 主布局
│       ├── router/                   # 路由
│       └── views/                   # Home/Realtime/History/Dashboard/ModelManager
├── model/                           # 深度学习模型
│   ├── models/
│   │   ├── resnet.py                # ResNet50 分类模型
│   │   └── yolo.py                  # YOLO11 检测 Predictor
│   ├── raw/                         # NEU-DET 原始数据集（6 类 bmp）
│   ├── train.py                     # ResNet 训练脚本
│   ├── train_yolo.py                # YOLO11 训练脚本
│   ├── evaluate.py                  # 测试集评估
│   ├── predict.py                   # ResNet Predictor
│   ├── neu_det.yaml                 # YOLO 数据集配置
│   └── config.py                    # 类别 / 超参 / 路径
├── docker/                          # 容器化部署
│   ├── backend/Dockerfile
│   ├── frontend/Dockerfile
│   └── nginx/nginx.conf
├── .gitignore
└── README.md




五、核心 API 一览

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | /predict | 上传图片检测，可在 Form 中传 model 切换模型 |
| GET | /video_feed | MJPEG 实时视频流 |
| POST | /camera/start | 启动摄像头采集 |
| POST |/camera/stop | 停止摄像头 |
| GET | /camera/status | 摄像头运行状态 + 当前模型信息 |
| GET | /model/list | 已注册模型列表 |
| GET | /model/current | 当前激活模型 |
| POST | /model/select | 切换当前激活模型 |
| POST | /model/reload_yolo | 训练完成后重新加载 YOLO 权重 |
| GET | /history | 历史检测记录（按当前模型过滤） |
| DELETE | /history/{id} | 删除单条历史 |
| GET | /statistics | 看板统计（总次数 / 今日 / 平均置信度 / 趋势 / 分类分布） |



六、数据集说明

使用 NEU-DET 钢材表面缺陷数据集，共 6 类：

| 缩写 | 英文 | 中文 |
| --- | --- | --- |
| Cr | Cracks | 裂纹 |
| In | Inclusion | 夹杂 |
| Pa | Patches | 斑块 |
| PS | Pitted Surface | 点蚀 |
| RS | Rolled-in Scale | 轧制氧化皮 |
| Sc | Scratches | 划痕 |

原始数据存放于 model/raw/{Cr,In,Pa,PS,RS,Sc}/，每类约 100~300 张 bmp 图像。


七、本地运行

后端

bash
cd backend

1. 单独装 CPU 版 PyTorch
pip install torch==2.8.0 torchvision==0.23.0 --index-url https://download.pytorch.org/whl/cpu

2. 装其余依赖
pip install -r requirements.txt

3. 启动
python app.py
默认监听 http://127.0.0.1:8000


前端

bash
cd frontend
npm install
npm run dev


Docker 部署

bash
后端镜像
docker build -t visionforge-backend -f docker/backend/Dockerfile .

前端镜像
docker build -t visionforge-frontend -f docker/frontend/Dockerfile .




八、后续规划

- [x] ResNet50 钢材缺陷分类模型训练完成
- [x] YOLO11 钢材缺陷检测模型训练完成
- [x] 后端 FastAPI 服务 + 多模型管理体系
- [x] 前端 Vue3 可视化（上传检测 / 实时检测 / 历史 / 看板 / 模型管理）
- [x] Docker 容器化部署
- [x] ROS2 七舵机机械臂仿真环境
- [x] 总线舵机硬件调试 + 串口指令控制
- [x] LLM Agent 下发舵机角度指令
- [x] 语音模式（语音 → LLM → 舵机动作）
- [ ] 采购剩余 6 个舵机 → 实物七自由度机械臂整机装配
- [ ] 打通"视觉检测 → 实体机械臂执行"完整具身闭环
- [ ] 接入 YOLOv12 / RT-DETR 等更多模型（架构已就绪，注册即可）



九、项目亮点

1. 工程化分层：API / Services / Model / Database 四层清晰，业务逻辑与请求响应解耦。
2. 可扩展多模型管理：ModelManager 统一入口 + 统一 Predictor 接口，新增模型零业务改动。
3. 具身智能闭环设计：不止做视觉，而是把视觉、决策（LLM Agent）、执行（舵机/机械臂）打通。
4. 全栈自研：从 PyTorch 训练、FastAPI 后端、Vue 前端、Docker 部署到 ROS2 仿真和硬件舵机调试全链路自己落地。
5. 真实工业场景：面向钢材表面缺陷这一真实工业质检需求，使用公开 NEU-DET 数据集。



> 项目持续迭代中，机械臂硬件到位后将完成整机联调，敬请期待。

