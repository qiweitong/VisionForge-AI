<template>

<el-menu

class="sidebar"

router

:default-active="$route.path"

>

<el-menu-item

v-for="item in menuList"

:key="item.path"

:index="item.path"

>

<el-icon>

<component :is="item.icon"/>

</el-icon>

<span>

{{item.title}}

</span>

</el-menu-item>

</el-menu>

</template>

<script setup>

import { ref } from "vue"

import {

House,

Document,

DataAnalysis,

VideoCamera,

Cpu,

Setting

} from "@element-plus/icons-vue"

const activeIndex = ref("/")
const menuList=[

{

title:"首页",

path:"/",

icon:House

},

{

title:"历史记录",

path:"/history",

icon:Document

},

{

title:"数据统计",

path:"/dashboard",

icon:DataAnalysis

},

{

title:"实时检测",

path:"/camera",

icon:VideoCamera

},

{

title:"模型管理",

path:"/model",

icon:Cpu

},

{

title:"系统设置",

path:"/setting",

icon:Setting

}

]
</script>

<style scoped>

.sidebar{

width:220px;

border-radius:10px;

}

/* 整个菜单容器 */
:deep(.el-menu--vertical) {
  height: 100vh;    /* 菜单高度铺满屏幕 */
  --el-menu-item-height: 66px; /* 统一控制每个菜单项高度（推荐用这个变量） */
}

/* 单独修改菜单项 */
:deep(.el-menu-item) {
  font-size: 20px;        /* 文字大小 */
  padding-left: 20px !important;
  
}

/* 图标大小 */
:deep(.el-menu-item .el-icon) {
  font-size: 18px;
  margin-right: 8px;
}


</style>