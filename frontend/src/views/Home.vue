<template>
<div class="layout-wrap">
  <div class="home">
    <div class="container">
      <div class="content">
        <UploadCard  @predictSuccess="handlePredictSuccess"/>
        <ResultCard :result="result"  :file-info="imageFileInfo"/>
      </div>
    </div>
  </div>
</div>
</template>

<script setup>
import UploadCard from '@/components/UploadCard.vue';
import ResultCard from '@/components/ResultCard.vue';
import {ref} from 'vue'

const result = ref(null)
const imageFileInfo = ref(null)

const handlePredictSuccess = (responseData, fileInfo) => {
    if (responseData.success) {
        result.value = responseData.data
        imageFileInfo.value = fileInfo
    }
}
</script>

<style scoped>
.layout-wrap{
  display: flex;
  min-height: 100vh;
}

.home{
  flex: 1;
  padding-top: 16px;
  padding-left: 20px;
  padding-right: 20px;
}
.container{
  margin-top: 12px;
}
.content{
  display: flex;
  justify-content: space-between;
  align-items:flex-start;
  gap:40px;
}
</style>
