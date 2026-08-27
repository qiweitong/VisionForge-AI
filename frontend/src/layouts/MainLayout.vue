<template>
  <div class="layout">
    <!-- 左侧侧边栏：直接顶到顶部 -->
    <Sidebar />
    <!-- 右侧区域：包含头部 + 页面主体 -->
    <div class="right-wrap">
      <Header />
      <main class="main">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import Header from "@/components/Header.vue"
import Sidebar from "@/components/Sidebar.vue"
</script>

<style scoped>
.layout {
  min-height: 100vh;
  background: #f4f7fb;
  margin: 0;
  display: flex; /* 左右并排：Sidebar | right-wrap */
}
.right-wrap {
  display: flex;
  flex-direction: column;
  flex: 1;
  
}
.main {
  flex: 1;
  padding: 30px;
}
.header{
    display:flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 30px;
    margin:0;
    /* 关键：让标题区域可以自由居中 */
    width: 100%;
}
</style>