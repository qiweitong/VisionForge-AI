<template>
  <el-card class="upload-card">
    <h2>上传图片</h2>
    <el-upload
      class="upload-area"
      :auto-upload="false"
      :show-file-list="false"
      :on-change="handleUploadChange"
    >
      <el-button type="primary">选择图片</el-button>
    </el-upload>
    <div v-if="imageUrl" class="preview">
      <img :src="imageUrl" alt="preview" />
    </div>
    <el-button
      type="primary"
      @click="startPredict"
      :loading="loading"
      class="detect-btn"
    >
      开始检测
    </el-button>
  </el-card>
</template>

<script setup>
import { ref, onUnmounted } from "vue";
import { ElMessage } from "element-plus";
import { predictImage } from "@/api/predict";

const imageUrl = ref("");
const emit = defineEmits(["predictSuccess"]);
const loading = ref(false);
const selectedFile = ref(null);
const fileSizeText = ref("");
let isDestroy = false;

const handleUploadChange = (file) => {
  if (!file) return;
  if (imageUrl.value) URL.revokeObjectURL(imageUrl.value);

  selectedFile.value = file.raw;
  imageUrl.value = URL.createObjectURL(file.raw);

  const byte = file.raw.size;
  if (!isNaN(byte) && byte > 0) {
    fileSizeText.value = (byte / 1024).toFixed(2) + " KB";
  } else {
    fileSizeText.value = "未知";
  }
};

const startPredict = async () => {
  if (!selectedFile.value) {
    ElMessage.warning("请先选择一张图片！");
    return;
  }
  loading.value = true;
  try {
    const response = await predictImage(selectedFile.value);
    emit("predictSuccess", response.data, {
      fileName: selectedFile.value.name,
      fileSize: fileSizeText.value
    });
    ElMessage.success("检测完成");
  } catch (error) {
    console.error("检测接口报错：", error);
    ElMessage.error("检测失败，请重新上传图片");
  } finally {
    if (!isDestroy) loading.value = false;
  }
};

onUnmounted(() => {
  isDestroy = true;
  if (imageUrl.value) URL.revokeObjectURL(imageUrl.value);
});
</script>

<style scoped>
.upload-card {
  width: 660px;
  min-height: 600px;
  box-shadow: 0 8px 25px rgba(0,0,0,.08);
}
.upload-card h2 {
  text-align: center;
  margin-bottom: 20px;
}
.preview {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
.preview img {
  max-width: 100%;
  max-height: 420px;
}
.detect-btn {
  width: 100%;
  margin-top: 30px;
  height: 48px;
  font-size: 18px;
}
</style>
