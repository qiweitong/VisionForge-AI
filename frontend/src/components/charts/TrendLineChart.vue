<template>
  <div ref="lineChartRef" style="width:100%;height:360px;"></div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch, computed, nextTick } from 'vue'
import * as echarts from 'echarts'

// 接收父组件传入数据
const props = defineProps({
  data: {
    type: Array,
    default: () => []
  }
})

const lineChartRef = ref(null)
let chartInstance = null

// 根据后端数据组装坐标轴与曲线数据
const chartSource = computed(() => {
  const xData = props.data.map(item => item.date)
  const yData = props.data.map(item => item.count)
  return { xData, yData }
})

// 更新绘图
const renderChart = () => {
  if (!chartInstance) return
  const { xData, yData } = chartSource.value
  const option = {
    xAxis: {
      type: "category",
      data: xData
    },
    yAxis: {
      type: "value"
    },
    series: [
      {
        type: "line",
        smooth: true,
        data: yData
      }
    ],
    tooltip: {
      trigger: 'axis'
    },
    grid: {
      left: 10,
      right: 10,
      bottom: 30
    }
  }
  chartInstance.setOption(option, true)
}

const initChart = () => {
  if (!lineChartRef.value) return
  chartInstance = echarts.init(lineChartRef.value)
  renderChart()
}

// 窗口自适应
const resizeHandler = () => {
  chartInstance?.resize()
}

// 监听父组件数据变化，自动刷新折线图
watch(chartSource, async () => {
  await nextTick()
  renderChart()
}, { deep: true })

onMounted(() => {
  nextTick(() => {
    initChart()
    window.addEventListener('resize', resizeHandler)
  })
})

// 销毁释放资源，解决 parentNode 报错
onBeforeUnmount(() => {
  window.removeEventListener('resize', resizeHandler)
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
})
</script>