<template>
<h2>📊 数据统计</h2>

<div class="model-indicator" v-if="currentModel">
    <el-tag :type="currentModel.task_type === 'classification' ? 'success' : 'warning'">
        当前模型: {{ currentModel.display_name }}
    </el-tag>
</div>

<div class="card-container">
    <el-card class="card">
        <h3>总检测次数</h3>
        <h1>{{ card.total }}</h1>
    </el-card>
    <el-card class="card">
        <h3>今日检测</h3>
        <h1>{{ card.today }}</h1>
    </el-card>
    <el-card class="card">
        <h3>平均置信度</h3>
        <h1>{{ card.avgConfidence }}%</h1>
    </el-card>
    <el-card class="card">
        <h3>平均推理时间</h3>
        <h1>{{ card.avgTime }} ms</h1>
    </el-card>
</div>

<div class="chart-wrap" style="margin-top:20px;">
    <el-row :gutter="20">
        <el-col :span="12">
            <el-card>
                <DefectBarChart :data="barData"/>
            </el-card>
        </el-col>
        <el-col :span="12">
            <el-card>
                <DefectPieChart :data="pieData"/>
            </el-card>
        </el-col>
    </el-row>
</div>

<el-row style="margin-top:20px">
    <el-col :span="24">
        <el-card>
            <TrendLineChart :data="trendData"/>
        </el-card>
    </el-col>
</el-row>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { getStatistics } from "@/api/statistics"
import { getCurrentModel } from "@/api/model"
import DefectBarChart from "@/components/charts/DefectBarChart.vue"
import DefectPieChart from "@/components/charts/DefectPieChart.vue"
import TrendLineChart from "@/components/charts/TrendLineChart.vue"

const card = ref({
  total: 0,
  today: 0,
  avgConfidence: 0,
  avgTime: 0
})
const barData = ref([])
const pieData = ref([])
const trendData = ref([])
const currentModel = ref(null)

const loadStatistics = async () => {
    try {
        const res = await getStatistics()
        if (res.data.success) {
            card.value = res.data.data.card
            barData.value = res.data.data.bar
            pieData.value = res.data.data.pie
            trendData.value = res.data.data.trend
        }
    } catch (err) {
        console.error("获取统计数据失败：", err)
    }
}

const loadCurrentModel = async () => {
    try {
        const res = await getCurrentModel()
        if (res.data.success) {
            currentModel.value = res.data.data
        }
    } catch (err) {
        console.error("获取当前模型失败：", err)
    }
}

onMounted(() => {
    loadStatistics()
    loadCurrentModel()
})
</script>

<style scoped>
.model-indicator {
    margin-bottom: 16px;
}

.card-container{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:20px;
    margin-top:20px;
}
.card{
    text-align:center;
}
.card h3{
    color:#888;
}
.card h1{
    font-size:42px;
    margin-top:20px;
    color:#409EFF;
}
</style>
