<template>
    <div class="chat-page-container">
        <div class="messages-container">
            <div v-for="(message, index) in messageList" :key="index" class="message-item"
                :style="'justify-content: ' + (message.isUser ? 'flex-end' : 'flex-start') + ';'">
                <div v-if="!message.isUser && message.isAnswer" class="answer-message" v-html="message.text"></div>
                <Collapse v-if="!message.isUser && !message.isAnswer && !message.isLoading" class="think-message"
                    :content="message.text">
                    <template #title>
                        <div>
                            <el-icon>
                                <Opportunity />
                            </el-icon>
                            <span>推理完成</span>
                        </div>
                    </template>
                </Collapse>
                <div v-if="message.isLoading" class="think-message">
                    <el-icon class="rotate-icon">
                        <Loading />
                    </el-icon>
                    {{ message.text }}
                </div>
                <div v-if="message.isUser" class="user-message">{{ message.text }}</div>

                <!-- <el-icon v-if="message.isUser">
                    <UserFilled />
                </el-icon> -->
            </div>
        </div>
        <div class="inputbar">
            <el-card shadow="never" class="input-section">
                <el-input type="textarea" autosize v-model="userInput" placeholder="请输入您的问题..." />
                <div class="input-buttons">
                    <div>
                        <el-icon class="more-options button" @click="voiceInput" title="语音输入">
                            <Microphone />
                        </el-icon>
                        <el-icon class="more-options button" @click="moreOptions" title="上传图片">
                            <Picture />
                        </el-icon>
                    </div>
                    <el-icon class="send-message button" @click="sendMessage" title="发送">
                        <Top />
                    </el-icon>
                </div>
            </el-card>
        </div>

        <el-dialog v-model="dialogVisible" title="语音输入">
            <el-button @click="startRecord" :disabled="startBtnDisabled">开始录音</el-button>
            <el-button @click="endRecord" :disabled="endBtnDisabled">结束录音</el-button>
            <div style="background: #f2f2f2;"> {{ recordStatus }}</div>
            <div>录音内容：</div>
            <div>{{ voiceRecord }}</div>
            <template #footer>
                <span class="dialog-footer">
                    <el-button type="primary" @click="closeDialog">完成</el-button>
                </span>
            </template>
        </el-dialog>
    </div>
</template>

<script setup>
import { ref, onMounted, getCurrentInstance } from 'vue';
// import { useRoute } from 'vue-router';
import { ElMessage } from 'element-plus'
import markdownit from 'markdown-it';
import Collapse from './Collapse.vue';

// const route = useRoute();
// const router = useRouter();
const userInput = ref("");
const messageList = ref([
    { text: '您好，我是您的医疗AI助手，请向我提问!', isUser: false, isAnswer: true },
]);
const { proxy } = getCurrentInstance();   //获取上下文
const md = markdownit(); //markdown格式转换

const sendMessage = () => {
    if (!userInput.value.trim()) { // 检查 userInput非空
        ElMessage.warning('输入内容不能为空');
        return;
    }
    messageList.value.push({ text: userInput.value, isUser: true });
    setTimeout(() => {
        botAnswer(userInput.value);
        userInput.value = "";
    }, 500);
};


const dialogVisible = ref(false);
const voiceRecord = ref('')
const startBtnDisabled = ref(false)
const endBtnDisabled = ref(true)
const recordStatus = ref('')

// 控制语音输入
const voiceInput = () => { dialogVisible.value = true;}
const closeDialog = () => { 
    dialogVisible.value = false;
    console.log(voiceRecord.value)
};

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


const moreOptions = () => {
    console.log("more options");
};

// 调用模型请求
const botAnswer = async (text) => {
    try {
        messageList.value.push({ text: '正在思考中...', isUser: false, isAnswer: false, isLoading: true });
        const response = await proxy.$axios.post('/send_input', { input_text: text });
        const res = response.data.response;
        const thinkContent = extractThinkContent(res);  // 提取思考内容
        const formalResponse = removeThinkTags(res);    // 提取回答内容
        messageList.value.pop();
        messageList.value.push({ text: thinkContent, isUser: false, isAnswer: false });
        messageList.value.push({ text: md.render(formalResponse), isUser: false, isAnswer: true });
        console.log(messageList.value);
    } catch (error) {
        console.error(error);
    }
}

// 提取 <think> 标签中的内容
const extractThinkContent = (response) => {
    const thinkStart = "<think>";
    const thinkEnd = "</think>";

    const startIdx = response.indexOf(thinkStart);
    const endIdx = response.indexOf(thinkEnd);

    // 如果找到了 <think> 标签，提取其中的内容
    if (startIdx !== -1 && endIdx !== -1) {
        return response.substring(startIdx + thinkStart.length, endIdx).trim();
    }

    // 否则返回空
    return null;
};

// 删除 <think> 标签并返回正式回复
const removeThinkTags = (response) => {
    const thinkStart = "<think>";
    const thinkEnd = "</think>";

    // 如果包含 <think> 标签，删除它
    const startIdx = response.indexOf(thinkStart);
    const endIdx = response.indexOf(thinkEnd);

    if (startIdx !== -1 && endIdx !== -1) {
        // 返回去除 <think> 标签后的文本
        return response.substring(0, startIdx) + response.substring(endIdx + thinkEnd.length);
    }

    return response; // 如果没有 <think> 标签，则直接返回原始响应
};
</script>

<style scoped>
.chat-page-container {
    height: 100%;
    width: 100%;
    position: relative;
}

.messages-container {
    height: calc(100% - 150px);
    overflow-y: auto;
    padding: 10px;
}

.message-item {
    margin-bottom: 10px;
    display: flex;
    text-align: left;
}

.message-item>div {
    padding: 10px;
    border-radius: 10px;
    max-width: 80%;
}

.user-message {
    background-color: #dcf8c6;
    margin-left: 30%;
}

.think-message {
    background-color: #d1d6db;
    margin-right: 30%;
    width: 80%;
}

/* 加载旋转动画 */
@keyframes rotate {
    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}

.rotate-icon {
    animation: rotate 1s linear infinite;
}

.answer-message {
    background-color: #e9ecef;
    margin-right: 30%;
}

.inputbar {
    bottom: 0;
    position: absolute;
    width: calc(100% - 40px);
    margin: 10px;
}

:deep(.el-card__body) {
    padding: 20px 20px 10px 20px !important;
}

.input-section {
    background-color: #f9f9f9;
}

.inputbar .el-card__body {
    padding: 10px !important;
}

.inputbar .el-textarea textarea {
    display: inline-block;
    background: none !important;
    border: none !important;
    outline: none;
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    font-size: 16px;
    color: #2b2b2b;
}

.inputbar .input-buttons {
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
}
</style>

<style>
/* 添加一些基本样式 */
.markdown-body {
    font-size: 16px;
    line-height: 1.6;
    color: #333;
}

.markdown-body h1 {
    font-size: 24px;
    margin-bottom: 10px;
}

.markdown-body ul {
    margin-left: 20px;
}

.markdown-body li {
    margin-bottom: 5px;
}

.markdown-body strong {
    font-weight: bold;
}

.markdown-body em {
    font-style: italic;
}

.markdown-body a {
    color: #007bff;
    text-decoration: none;
}

.markdown-body a:hover {
    text-decoration: underline;
}

.markdown-body pre {
    background-color: #f4f4f4;
    border-radius: 5px;
    padding: 10px;
    overflow-x: auto;
}

.markdown-body code {
    font-family: "Courier New", Courier, monospace;
    background-color: #f1f1f1;
    padding: 2px 6px;
    border-radius: 3px;
}
</style>