from fastapi import FastAPI
# 新增跨域中间件导入
from fastapi.middleware.cors import CORSMiddleware
from api.predict import router as predict_router
import uvicorn

app = FastAPI(
    title="VisionForge AI",
    version="1.0.0"
)

# ========== 新增跨域配置 ==========
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发环境允许所有前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# =================================

app.include_router(predict_router)


@app.get("/")
def root():
    return {
        "message": "VisionForge AI Backend Running!"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)