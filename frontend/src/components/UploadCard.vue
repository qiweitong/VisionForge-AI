<template>
  <el-card class="upload-card">
    <h2>上传图片</h2>

    <input
      type="file"
      accept="image/*"
      @change="handleFileChange"
    />

    <div
      v-if="imageUrl"
      class="preview"
    >
      <img
        :src="imageUrl"
        alt="preview"
      />
    </div>
    <!-- 修复：属性中间加空格 -->
    <el-button
      type="primary"
      @click="startPredict"
      :loading="loading"
      class="detect-btn"
    >
      开始检测
    </el-button>
  </el-card>

  <div
    v-if="result"
    class="result"
>

    <h3>检测结果</h3>

    <p>
        缺陷：
        {{ result.data.class_name }}
    </p>

    <p>
        置信度：

        {{ (result.data.confidence*100).toFixed(2) }} %

    </p>

    <p>

        推理时间：

        {{ result.data.inference_time }} ms

    </p>

</div>
</template>

<script setup>
import { ref, onUnmounted } from "vue";
import { ElMessage } from "element-plus"; // 新增弹窗提示
import { predictImage } from "@/api/predict"

const imageUrl = ref("");
const result = ref(null)
const loading = ref(false)
const selectedFile = ref(null)
let isDestroy = false

const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (!file) return;

  // 释放旧图片内存，避免异常
  if (imageUrl.value) URL.revokeObjectURL(imageUrl.value)

  selectedFile.value = file;
  imageUrl.value = URL.createObjectURL(file)
};

const startPredict = async () => {
  // 没上传图片给用户提示
  if (!selectedFile.value) {
    ElMessage.warning("请先选择一张图片！")
    return;
  }
  loading.value = true;

  try {
    const res = await predictImage(selectedFile.value);
    result.value = res;
    ElMessage.success("检测完成");
    console.log("检测结果：", result.value);
  } catch (error) {
    console.error("检测接口报错：", error);
    ElMessage.error("检测失败，请重新上传图片");
  } finally {
    // 组件销毁就不修改loading，防止报错
    if (!isDestroy) loading.value = false;
  }
}

// 组件销毁清理资源，解决之前 flags 报错
onUnmounted(() => {
  isDestroy = true
  if (imageUrl.value) URL.revokeObjectURL(imageUrl.value)
})
</script>

<style scoped>
.upload-card {
  width: 500px;
  padding: 20px;
}

.preview {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.preview img {
  width: 100%;
  max-height: 350px;
  object-fit: contain;
  border-radius: 8px;
}

.detect-btn {
  margin-top: 20px;
  width: 100%;
}

.result{

    margin-top:20px;

    padding:15px;

    border-radius:8px;

    background:pink;

}
</style>