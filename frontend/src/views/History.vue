<template>

<el-card>

<h2>历史记录</h2>

<div class="model-indicator" v-if="currentModel">
    <el-tag :type="currentModel.task_type === 'classification' ? 'success' : 'warning'">
        当前模型: {{ currentModel.display_name }}
    </el-tag>
</div>

<el-table :data="history" style="width:100%">

<el-table-column
prop="image_name"
label="图片"
width="180"
/>

<el-table-column
prop="class_cn"
label="缺陷"
/>

<el-table-column
prop="confidence"
label="置信度"
>
<template #default="scope">
{{(scope.row.confidence*100).toFixed(2)}}%
</template>
</el-table-column>

<el-table-column
prop="inference_time"
label="推理(ms)"
/>

<el-table-column
prop="model_name"
label="模型"
>
<template #default="scope">
<el-tag size="small">{{ scope.row.model_name }}</el-tag>
</template>
</el-table-column>

<el-table-column
prop="create_time"
label="检测时间"
/>

</el-table>

</el-card>

</template>

<script setup>

import {ref,onMounted} from "vue"

import {getHistory} from "@/api/history"
import {getCurrentModel} from "@/api/model"

const history=ref([])
const currentModel = ref(null)

const loadHistory=async()=>{
const res=await getHistory()
if (res.data.success) {
history.value=res.data.data
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

onMounted(()=>{
loadHistory()
loadCurrentModel()
})

</script>

<style scoped>
.model-indicator {
    margin-bottom: 16px;
}
</style>
