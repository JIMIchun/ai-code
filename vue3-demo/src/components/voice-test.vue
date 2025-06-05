<template>
  <div class="test-container">
    <el-button @click="startRecord" :disabled="startBtnDisabled">开始录音</el-button>
    <el-button @click="endRecord" :disabled="endBtnDisabled">结束录音</el-button>
    <div style="background: #f2f2f2;"> {{ recordStatus }}</div>
    <div>录音内容：</div>
    <div>{{ voiceRecord }}</div>
  </div>
</template>

<script setup>
import { ref, getCurrentInstance} from 'vue'

const { proxy } = getCurrentInstance(); 

const voiceRecord = ref('')
const startBtnDisabled = ref(false)
const endBtnDisabled = ref(true)
const recordStatus = ref('')

const startRecord = () => {
    endBtnDisabled.value = false
    startBtnDisabled.value = true
    proxy.$axios.post('/start_record').then(res => {
        if(res.data.status ==='success') {
            recordStatus.value = '录音中...'
        } else {
            recordStatus.value = `错误：${res.data.message}`
        }
    })
        .catch(() => {
            recordStatus.value = '启动录音失败</span>';
            resetButtons();
        });
}

const endRecord = () => {
    recordStatus.value = '转换中...'
    proxy.$axios.post('/stop_record').then(res => {
            if(res.data.status === 'success') {
                recordStatus.value = '转换结束！'
                voiceRecord.value = res.data.result.text;
            } else {
                recordStatus.value = `错误：${res.data.message}`;
            }
        })
        .catch(() => {
            recordStatus.value = '请求失败</span>';
        })
    resetButtons();
}

const resetButtons = () => {
    endBtnDisabled.value = true
    startBtnDisabled.value = false
}


</script>

<style scoped>
.test-container {
    height: 100%;
}

</style>
