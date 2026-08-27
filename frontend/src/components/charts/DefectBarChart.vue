<template>
  <div ref="chartDom" style="width:100%;height:400px;"></div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount, nextTick } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  data: {
    type: Array,
    default: () => []
  }
})

const chartDom = ref(null)
let chartInstance = null

// 渲染图表（只负责setOption，数据更新统一调用这个方法）
const renderChart = () => {
  if (!chartInstance) return

  const xData = props.data.map(item => item.class_cn)
  const yData = props.data.map(item => item.count)

  const option = {
    tooltip: {},
    xAxis: { type: 'category', data: xData },
    yAxis: { type: 'value' },
    series: [{
      type: 'bar',
      data: yData
    }]
  }
  // true：不合并旧配置，强制刷新图表
  chartInstance.setOption(option, true)
}

// 初始化echarts实例，只在挂载时执行一次
const initChart = () => {
  if (!chartDom.value) return
  chartInstance = echarts.init(chartDom.value)
  renderChart()
}

// 监听父组件传入的数据变化 → 触发重新渲染
watch(
  () => props.data,
  () => {
    nextTick(renderChart)
  },
  { deep: true } 
  // 👉 优化提示：
  // 父组件直接赋值 data = [...新数组] → 删除 deep:true
  // 父组件只修改数组内对象属性，例如data[0].count=100 → 保留 deep:true
)

onMounted(() => {
  nextTick(initChart)
})

// 组件销毁，释放echarts实例，解决常见报错：Cannot read properties of null (reading 'parentNode')
onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
})
</script>

<style scoped>
/* template没有使用class="chart"，该样式无效，直接删除 */
</style>