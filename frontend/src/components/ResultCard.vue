<template>
  <el-card class="result-card" shadow="never">
    <h2>检测结果</h2>

    <div v-if="result">
      <!-- 分类结果展示 -->
      <template v-if="result.task_type === 'classification'">
        <el-descriptions :column="1" border size="large">
          <el-descriptions-item label="缺陷类别">
            <el-tag type="success" size="large">
              {{ result.class_name }}
            </el-tag>
          </el-descriptions-item>

          <el-descriptions-item label="缺陷名称">
            {{ classMap[result.class_name] || result.class_cn || '未知缺陷' }}
          </el-descriptions-item>

          <el-descriptions-item label="置信度">
            {{ confidenceText }} %
            <el-progress
              :text-inside="true"
              :stroke-width="22"
              :percentage="progressValue"
            />
          </el-descriptions-item>

          <el-descriptions-item label="推理时间">
            {{ result.inference }} ms
          </el-descriptions-item>

          <el-descriptions-item label="图片大小">
            {{ fileInfo?.fileSize }}
          </el-descriptions-item>

          <el-descriptions-item label="模型名称">
            {{ result.model_display || 'Classification' }}
          </el-descriptions-item>
        </el-descriptions>
      </template>

      <!-- 检测结果展示 -->
      <template v-else-if="result.task_type === 'detection'">
        <el-descriptions :column="1" border size="large">
          <el-descriptions-item label="检测模型">
            <el-tag type="warning" size="large">
              {{ result.model_display || 'Detection' }}
            </el-tag>
          </el-descriptions-item>

          <el-descriptions-item label="检测数量">
            <span style="font-size: 24px; font-weight: bold; color: #409eff;">
              {{ result.detections?.length || 0 }}
            </span>
          </el-descriptions-item>

          <el-descriptions-item label="推理时间">
            {{ result.inference }} ms
          </el-descriptions-item>

          <el-descriptions-item label="图片大小">
            {{ fileInfo?.fileSize }}
          </el-descriptions-item>
        </el-descriptions>

        <div v-if="result.detections && result.detections.length > 0" class="detection-list">
          <h3>检测详情</h3>
          <el-table :data="result.detections" stripe size="small" max-height="300">
            <el-table-column type="index" label="#" width="50" />
            <el-table-column prop="class_name" label="类别" width="100">
              <template #default="scope">
                <el-tag>{{ scope.row.class_name }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="class_cn" label="名称" width="100" />
            <el-table-column prop="confidence" label="置信度" width="150">
              <template #default="scope">
                {{ (scope.row.confidence * 100).toFixed(2) }}%
                <el-progress
                  :percentage="scope.row.confidence * 100"
                  :stroke-width="10"
                  :show-text="false"
                  style="display: inline-block; width: 80px; margin-left: 8px;"
                />
              </template>
            </el-table-column>
            <el-table-column label="坐标">
              <template #default="scope">
                [{{ scope.row.bbox?.join(', ') }}]
              </template>
            </el-table-column>
          </el-table>
        </div>

        <el-empty v-else description="未检测到任何缺陷" />
      </template>
    </div>

    <div v-else class="empty-container">
      <el-empty description="请上传图片进行检测" />
    </div>
  </el-card>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  result: Object,
  fileInfo: Object
})

const classMap = {
  Cr: "裂纹",
  In: "夹杂",
  Pa: "斑块",
  PS: "点蚀",
  RS: "轧制氧化皮",
  Sc: "划痕",
  crazing: "裂纹",
  inclusion: "夹杂",
  patches: "斑块",
  pitted_surface: "点蚀",
  "rolled-in_scale": "轧制氧化皮",
  scratches: "划痕"
}

const confidenceText = computed(() => {
  const num = Number(props.result?.confidence ?? 0)
  return (num * 100).toFixed(2)
})

const progressValue = computed(() => {
  const num = Number(props.result?.confidence ?? 0)
  const val = num * 100
  return Math.max(0, Math.min(val, 100))
})
</script>

<style scoped>
.result-card {
  width: 660px;
  min-height: 600px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
}

.result-card h2 {
  margin-bottom: 30px;
  text-align: center;
}

.detection-list {
  margin-top: 20px;
}

.detection-list h3 {
  margin-bottom: 12px;
  color: #606266;
}
</style>
