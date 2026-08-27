<template>
<div class="realtime">
    <el-row :gutter="20">
        <el-col :span="18">
            <el-card>
                <template #header>
                    <span>🎥 实时检测</span>
                </template>
                <img
                    v-show="streamUrl"
                    class="camera"
                    :src="streamUrl"
                    crossorigin="anonymous"
                />
                <div v-if="!streamUrl" style="height:480px;background:#f5f7fa;display:flex;align-items:center;justify-content:center;color:#999;border-radius:10px;">
                    摄像头未开启
                </div>
            </el-card>
        </el-col>

        <el-col :span="6">
            <el-card>
                <template #header>
                    <span>控制面板</span>
                </template>

                <el-descriptions :column="1" border>
                    <el-descriptions-item label="状态">
                        {{ statusData.running ? '🟢 Running' : '🔴 Stopped' }}
                    </el-descriptions-item>
                    <el-descriptions-item label="模型">
                        <el-tag :type="statusData.task_type === 'classification' ? 'success' : 'warning'">
                            {{ statusData.model || 'N/A' }}
                        </el-tag>
                    </el-descriptions-item>
                    <el-descriptions-item label="类型">
                        {{ statusData.task_type === 'classification' ? '分类' : '检测' }}
                    </el-descriptions-item>
                    <el-descriptions-item label="类别/数量">
                        {{ statusData.cls }}
                    </el-descriptions-item>
                    <el-descriptions-item label="置信度">
                        {{ (statusData.confidence * 100).toFixed(2) }}%
                    </el-descriptions-item>
                    <el-descriptions-item label="FPS">
                        {{ statusData.fps }}
                    </el-descriptions-item>
                </el-descriptions>

                <el-divider />

                <el-button
                    type="success"
                    style="width:100%;margin-bottom:10px;"
                    @click="startCamera"
                    :disabled="!!streamUrl"
                >
                    开始检测
                </el-button>

                <el-button
                    type="danger"
                    style="width:100%;margin-left:0;margin-bottom:10px;"
                    @click="stopCamera"
                    :disabled="!streamUrl"
                >
                    停止检测
                </el-button>

                <el-button style="width:100%;margin-left:0;">
                    保存截图
                </el-button>
            </el-card>
        </el-col>
    </el-row>
</div>
</template>

<script setup>
import { ref, onUnmounted, nextTick, onMounted } from 'vue'
import axios from 'axios'
import { getCurrentModel } from '@/api/model'

const API_HOST = "http://127.0.0.1:8000"
const baseStream = `${API_HOST}/video_feed`
const streamUrl = ref('')

const statusData = ref({
  running: false,
  cls: "None",
  confidence: 0,
  fps: 0,
  model: "Loading...",
  task_type: "unknown"
})
let pollTimer = null

const loadModelInfo = async () => {
  try {
    const res = await getCurrentModel()
    if (res.data.success && res.data.data) {
      statusData.value.model = res.data.data.display_name
      statusData.value.task_type = res.data.data.task_type
    }
  } catch (e) {
    console.error("获取模型信息失败:", e)
  }
}

const startCamera = async () => {
  streamUrl.value = ''
  await nextTick()

  await axios.post(`${API_HOST}/camera/start`)
  await new Promise(resolve => setTimeout(resolve, 500))
  const ts = Date.now()
  streamUrl.value = `${baseStream}?t=${ts}`

  startPoll()
}

const stopCamera = async () => {
  try {
    await axios.post(`${API_HOST}/camera/stop`)
  } catch (e) {
    console.error("停止异常", e)
  } finally {
    streamUrl.value = ''
    stopPoll()
    statusData.value = {
      running: false,
      cls: "None",
      confidence: 0,
      fps: 0,
      model: statusData.value.model,
      task_type: statusData.value.task_type
    }
  }
}

const startPoll = () => {
  stopPoll()
  pollTimer = setInterval(async () => {
    try {
      const res = await axios.get(`${API_HOST}/camera/status`)
      statusData.value.running = res.data.running
      statusData.value.cls = res.data.class
      statusData.value.confidence = res.data.confidence
      statusData.value.fps = res.data.fps
      if (res.data.model) {
        statusData.value.model = res.data.model
      }
      if (res.data.task_type) {
        statusData.value.task_type = res.data.task_type
      }
    } catch (err) {
      // fail silently
    }
  }, 200)
}

const stopPoll = () => {
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
}

onMounted(() => {
  loadModelInfo()
})

onUnmounted(() => {
  stopPoll()
  if (streamUrl.value) {
    stopCamera()
  }
})
</script>

<style scoped>
.realtime {
    padding: 20px;
}

.camera {
    width: 100%;
    border-radius: 10px;
}
</style>
