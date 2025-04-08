<template>
    <div class="content-container">
        <div class="content">
            <div class="title">
                <el-icon size="35px">
                    <Promotion />
                </el-icon>
                IMRIS医疗辅助助手
            </div>
            <el-card shadow="never" class="input-section">
                <el-input type="textarea" :rows="2" v-model="userInput" placeholder="输入问题，向我提问" />
                <div class="input-buttons">
                    <el-icon class="more-options button" @click="moreOptions" title="More">
                        <Plus />
                    </el-icon>
                    <el-icon class="send-message  button" @click="sendMessage" title="Send message">
                        <Top />
                    </el-icon>
                </div>
            </el-card>
            <div class="suggestions">
                <p style="margin: 0; font-size: 14px; color: #c1c1c1;">
                    <el-icon>
                        <MagicStick />
                    </el-icon> 建议
                </p>
                <el-card class="box-card" v-for="(sugg, index) in suggList" :key="index" shadow="hover"
                    :title="sugg.text" @click="userInput = sugg.text">
                    <template #header>
                        <span>{{ sugg.title }}</span>
                    </template>
                    <span>{{ sugg.text }}</span>
                </el-card>
            </div>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue';

export default {
    name: 'BlankPage',
    props: {
        selectModel: String,
    },
    setup(props, { emit }) {
        const userInput = ref('');
        const suggList = [
            { title: '新辅助治疗前的评估流程', text: '请详细描述新辅助治疗前的评估流程，包括影像学检查的具体应用，以及如何评估腋窝淋巴结状态和全身潜在转移病灶。' },
            { title: '适合新辅助治疗的乳腺癌患者', text: '详细说明如何筛选适合新辅助治疗的患者，包括必选人群、优选人群和可选人群的标准，以及需要考虑的临床因素（如肿瘤负荷、病理学特征等）。' }
        ];

        const sendMessage = () => {
            emit('send-message', { model: props.selectModel, userInput: userInput.value });
        };

        const moreOptions = () => {
            console.log('more options');
        };

        // 如果有watch，需要在这里定义

        return {
            userInput,
            suggList,
            sendMessage,
            moreOptions,
        };
    },
};
</script>

<style scoped>
.content-container {
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}

.content {
    width: 50%;
    height: fit-content;
    padding: 20px;
}

.content .title {
    font-size: 45px;
    text-align: center;
    margin-bottom: 20px;
    font-weight: bold;
}

.content .input-section {
    background-color: #f9f9f9;
    border-radius: 10px;
    border: none;
}

:deep(.el-card__body) {
    padding: 20px 20px 10px 20px !important;
}

.el-textarea textarea {
    display: inline-block;
    background: none !important;
    border: none !important;
    outline: none;
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    font-size: 16px;
    color: #2b2b2b;
}

.content .input-buttons {
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
}

.content .suggestions {
    font-size: 14px;
    margin-top: 10px;
    line-height: 1.4;
    padding-left: 20px;
    text-align: left;
}

.content .suggestions .el-card {
    border: none;
    margin-bottom: 5px;
    color: #6d6d6d;
    padding: 5px;
    cursor: pointer;
}

:deep(.el-card__header) {
    padding: 0px;
    border: none;
    font-size: 17px;
    font-weight: bold;
}

:deep(.el-card__body) {
    padding: 0px;
    border: none;
}

:deep(.el-card__body span) {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    width: 100%;
    display: inline-block;
}
</style>
