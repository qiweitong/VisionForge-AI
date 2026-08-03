<template>

<div class="container">

    <h1>VisionForge AI</h1>

    <UploadCard />
</div>

</template>

<script setup>
import UploadCard from '@/components/UploadCard.vue';


</script>

<style scoped>

.container{

    min-height:100vh;

    display:flex;

    flex-direction:column;

    align-items:center;

    padding-top:40px;

    gap:30px;

}



</style>