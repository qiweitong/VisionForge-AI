<template>
<header class="header">
    <div class="title-wrap">
        <h1>VisionForge AI</h1>
        <p>Industrial Defect Detection System</p>
    </div>
    <div class="status" @click="goToModelManager" style="cursor: pointer;">
        🟢 {{ currentModel?.display_name || 'Loading...' }}
    </div>
</header>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getCurrentModel } from '@/api/model'

const router = useRouter()
const currentModel = ref(null)

const loadModelInfo = async () => {
    try {
        const res = await getCurrentModel()
        if (res.data.success && res.data.data) {
            currentModel.value = res.data.data
        }
    } catch (e) {
        console.error("获取模型信息失败:", e)
    }
}

const goToModelManager = () => {
    router.push('/model')
}

onMounted(() => {
    loadModelInfo()
})
</script>

<style scoped>
.header{
    display:flex;
    align-items: center;
    padding: 0 30px;
    margin:0;
    position: relative;
    width: 100%;
    min-height: 120px;
}
.title-wrap{
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -30%);
    text-align: center;
}
.header h1{
    font-size:48px;
    color:#409EFF;
    margin:0;
}
.header p{
    margin-top:10px;
    color:#777;
}
.status{
    margin-left: auto;
    background:#ecfdf5;
    color:#16a34a;
    padding:8px 18px;
    border-radius:20px;
    font-weight:bold;
}
</style>
