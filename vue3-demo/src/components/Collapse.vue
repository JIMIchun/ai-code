<template>
  <div class="collapse-panel">
    <div class="collapse-header" @click="toggleCollapse">
      <slot name="title"><span>{{ title }}</span></slot>
      <el-icon :class="['arrow-icon', { 'is-collapsed': isCollapsed }]">
        <ArrowDown />
      </el-icon>
    </div>
    <transition name="slide">
      <div v-show="!isCollapsed" class="collapse-content">
        {{ content }}
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ArrowDown } from '@element-plus/icons-vue'

const props = defineProps({
  title: {
    type: String,
    required: true,
    default: '标题'
  },
  content: {
    type: String,
    required: true,
    default: '内容'
  }
})

const isCollapsed = ref(true)

const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value
}
</script>

<style scoped>
.collapse-panel {
  /* border: 1px solid #ebeef5; */
  border-radius: 4px;
  margin-bottom: 10px;
  overflow: hidden;
}

.collapse-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  /* padding: 12px 16px; */
  /*background-color: #f5f7fa;*/
  cursor: pointer;
  transition: all 0.3s;
}

/*.collapse-header:hover {
   background-color: #f0f2f5; 
}*/

.arrow-icon {
  transition: transform 0.3s;
}

.arrow-icon.is-collapsed {
  transform: rotate(-90deg);
}

.collapse-content {
  padding: 16px;
  /* background-color: #f5f7fa; */
}

/* 动画效果 */
.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
  max-height: 500px; /* 设置一个足够大的值 */
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  max-height: 0;
  padding-top: 0;
  padding-bottom: 0;
}
</style>
