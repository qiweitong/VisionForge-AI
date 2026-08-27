<template>
  <!-- 图表容器，必须给定宽高 -->
  <div ref="pieChartRef" style="width:100%;height:400px;"></div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch, computed, nextTick } from 'vue'
import * as echarts from 'echarts'

// 接收父组件 Dashboard 传过来的数据
const props = defineProps({
  data: {
    type: Array,
    default: () => []
  }
})

const pieChartRef = ref(null)
let chartInstance = null

// 把后端数组转换成 echarts 需要的 {name,value} 格式
const chartData = computed(() => {
  return props.data.map(item => ({
    name: item.class_cn,
    value: item.count
  }))
})

// 渲染图表
const renderChart = () => {
  if (!chartInstance) return
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    series: [
      {
        type: "pie",
        radius: "65%",
        data: chartData.value
      }
    ]
  }
  chartInstance.setOption(option, true)
}

// 初始化图表
const initChart = () => {
  if (!pieChartRef.value) return
  chartInstance = echarts.init(pieChartRef.value)
  renderChart()
}

// 窗口自适应
const resizeHandler = () => {
  chartInstance?.resize()
}

// 监听父组件数据变化，自动刷新饼图
watch(chartData, async () => {
  await nextTick()
  renderChart()
}, { deep: true })

onMounted(() => {
  nextTick(() => {
    initChart()
    window.addEventListener('resize', resizeHandler)
  })
})

// 页面销毁清理资源，解决 parentNode 报错
onBeforeUnmount(() => {
  window.removeEventListener('resize', resizeHandler)
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
})
</script>