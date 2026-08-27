<template>
<div class="model-manager">
    <el-row :gutter="20">
        <el-col :span="16">
            <el-card>
                <template #header>
                    <div class="card-header">
                        <span>🧠 模型管理</span>
                        <el-button
                            type="primary"
                            size="small"
                            @click="loadModels"
                            :loading="loading"
                        >
                            刷新
                        </el-button>
                    </div>
                </template>

                <div v-if="models.length === 0" class="empty-state">
                    <el-empty description="暂无可用模型" />
                </div>

                <div v-else class="model-list">
                    <el-card
                        v-for="model in models"
                        :key="model.name"
                        class="model-card"
                        :class="{ active: model.is_current }"
                        shadow="hover"
                        @click="handleSelect(model)"
                    >
                        <div class="model-info">
                            <div class="model-name">
                                <el-tag
                                    :type="model.task_type === 'classification' ? 'success' : 'warning'"
                                    size="large"
                                >
                                    {{ model.task_type === 'classification' ? '分类模型' : '检测模型' }}
                                </el-tag>
                                <span class="display-name">{{ model.display_name }}</span>
                            </div>
                            <div class="model-meta">
                                <span>模型ID: {{ model.name }}</span>
                            </div>
                            <div class="model-status">
                                <el-tag
                                    v-if="model.is_current"
                                    type="success"
                                    effect="dark"
                                >
                                    当前使用中
                                </el-tag>
                                <el-button
                                    v-else
                                    type="primary"
                                    size="small"
                                    @click.stop="handleSelect(model)"
                                >
                                    切换到此模型
                                </el-button>
                            </div>
                        </div>
                    </el-card>
                </div>
            </el-card>
        </el-col>

        <el-col :span="8">
            <el-card>
                <template #header>
                    <span>当前模型状态</span>
                </template>

                <el-descriptions v-if="currentModel" :column="1" border>
                    <el-descriptions-item label="模型名称">
                        {{ currentModel.display_name }}
                    </el-descriptions-item>
                    <el-descriptions-item label="模型类型">
                        {{ currentModel.task_type === 'classification' ? '分类' : '检测' }}
                    </el-descriptions-item>
                    <el-descriptions-item label="模型ID">
                        {{ currentModel.name }}
                    </el-descriptions-item>
                </el-descriptions>

                <el-empty v-else description="未选择模型" />
            </el-card>

            <el-card style="margin-top: 20px;">
                <template #header>
                    <span>训练控制</span>
                </template>
                <el-button
                    type="warning"
                    style="width: 100%;"
                    @click="handleReloadYolo"
                    :loading="reloading"
                >
                    重新加载YOLO权重
                </el-button>
                <p class="tip">
                    训练完成后点击此按钮加载新权重
                </p>
            </el-card>
        </el-col>
    </el-row>
</div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getModelList, getCurrentModel, selectModel, reloadYolo } from '@/api/model'

const models = ref([])
const currentModel = ref(null)
const loading = ref(false)
const reloading = ref(false)

const loadModels = async () => {
    loading.value = true
    try {
        const res = await getModelList()
        models.value = res.data.data
    } catch (err) {
        console.error("加载模型列表失败:", err)
    } finally {
        loading.value = false
    }
}

const loadCurrentModel = async () => {
    try {
        const res = await getCurrentModel()
        if (res.data.success) {
            currentModel.value = res.data.data
        }
    } catch (err) {
        console.error("获取当前模型失败:", err)
    }
}

const handleSelect = async (model) => {
    try {
        const res = await selectModel(model.name)
        if (res.data.success) {
            ElMessage.success(`已切换到 ${model.display_name}`)
            await loadModels()
            await loadCurrentModel()
        }
    } catch (err) {
        ElMessage.error("切换模型失败")
    }
}

const handleReloadYolo = async () => {
    reloading.value = true
    try {
        const res = await reloadYolo()
        if (res.data.success) {
            ElMessage.success("YOLO权重重新加载成功")
            await loadModels()
            await loadCurrentModel()
        }
    } catch (err) {
        ElMessage.error("重新加载失败，请确认训练完成")
    } finally {
        reloading.value = false
    }
}

onMounted(() => {
    loadModels()
    loadCurrentModel()
})
</script>

<style scoped>
.model-manager {
    padding: 20px;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.model-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.model-card {
    cursor: pointer;
    transition: all 0.3s;
    border: 2px solid transparent;
}

.model-card:hover {
    transform: translateY(-2px);
}

.model-card.active {
    border-color: #409eff;
    background: linear-gradient(135deg, #ecf5ff 0%, #f0f9ff 100%);
}

.model-info {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.model-name {
    display: flex;
    align-items: center;
    gap: 12px;
}

.display-name {
    font-size: 18px;
    font-weight: bold;
    color: #303133;
}

.model-meta {
    color: #909399;
    font-size: 13px;
}

.model-status {
    margin-top: 8px;
}

.empty-state {
    padding: 40px;
}

.tip {
    margin-top: 12px;
    font-size: 12px;
    color: #909399;
    text-align: center;
}
</style>
