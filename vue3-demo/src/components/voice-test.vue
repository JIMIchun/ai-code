<template>
    <div class="test-container">
        <el-button @click="startRecord" :disabled="startBtnDisabled">开始录音</el-button>
        <el-button @click="endRecord" :disabled="endBtnDisabled">结束录音</el-button>
        <div style="background: #f2f2f2;"> {{ recordStatus }}</div>
        <div>录音内容：</div>
        <div>{{ voiceRecord }}</div>


        <div>
            <div>session对话列表测试</div>
            <el-button @click="newSession">new session</el-button>
            <el-button @click="getSessions">get sessions</el-button>
            <el-button @click="newMessage">new message</el-button>
            <el-button @click="getMessages">get messages</el-button>
        </div>
    </div>
</template>

<script setup>
import { ref, getCurrentInstance } from 'vue'

import { IdentityType, MessageType } from '../assets/enums'

const { proxy } = getCurrentInstance();

const voiceRecord = ref('')
const startBtnDisabled = ref(false)
const endBtnDisabled = ref(true)
const recordStatus = ref('')

const startRecord = () => {
    endBtnDisabled.value = false
    startBtnDisabled.value = true
    proxy.$axios.post('/start_record').then(res => {
        if (res.data.status === 'success') {
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
        if (res.data.status === 'success') {
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

const newSession = () => {
    proxy.$axios.post('/new_session', { patient_id: '1', title: '测试session测试session测试session测试session测试session测试session' }).then(res => {
        if (res.status === 201) {
            // 新对话创建成功
            console.log(res.data)
        }
    })
}

const getSessions = () => {
    proxy.$axios.get('/get_sessions/2').then(res => {
        if (res.status === 200) {
            // 获取对话列表成功
            console.log(res.data)
        }
    })
}

const newMessage = () => {
    proxy.$axios.post('/new_message', {
        session_id: '5',
        identity_type: IdentityType.MODEL,
        message_type: MessageType.TEXT,
        content: '测试消息1',
        inference: '测试消息1的推理结果'
    }).then(res => {
        if (res.status === 201) {
            // 设置消息成功
            console.log(res.data)
        }
    })
}

const getMessages = () => {
    proxy.$axios.get('/get_messages/1').then(res => {
        if (res.status === 200) {
            // 获取消息成功
            console.log(res.data)
        }
    })
}


</script>

<style scoped>
.test-container {
    height: 100%;
}
</style>
