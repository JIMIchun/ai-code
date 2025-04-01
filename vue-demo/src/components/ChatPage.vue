<template>
    <div class="chat-page-container">
        <div class="messages-container">
            <div v-for="(message, index) in messageList" :key="index" class="message-item"
                :class="{ 'user-message': message.isUser, 'bot-message': !message.isUser }">
                <i v-if="!message.isUser" class="el-icon-s-opportunity"></i>
                {{ message.text }}
                <i v-if="message.isUser" class="el-icon-s-custom"></i>
            </div>
        </div>

        <div class="inputbar">
            <el-card shadow="never" class="input-section">
                <el-input type="textarea" autosize v-model="userInput" placeholder="Enter your question" />
                <div class="input-buttons">
                    <div class="more-options el-icon-plus button" @click="moreOptions" title="More"></div>
                    <div class="send-message el-icon-top button" @click="sendMessage" title="Send message"></div>
                </div>
            </el-card>
        </div>
    </div>
</template>

<script>
export default {
    mounted() {
        console.log(this.$route.query);
        this.messageList.push({ text: this.$route.query.userInput, isUser: true });
        this.botAnswer();
    },
    data() {
        return {
            userInput: "",
            messageList: [
                { text: 'Send me messages!', isUser: false },
            ]
        };
    },
    methods: {
        moreOptions() {
            console.log("more options");
        },
        sendMessage() {
            this.messageList.push({ text: this.userInput, isUser: true });
            this.userInput = "";
            setTimeout(() => {
                this.botAnswer();
            }, 500);
        },
        botAnswer() {
            //TODO: 调用
            this.messageList.push({ text: 'I am a bot!', isUser: false });
            console.log(this.messageList);
        },
    },
}
</script>

<style scoped>
.chat-page-container {
    height: 100%;
    width: 100%;
    position: relative;
}

.messages-container {
    height: calc(100% - 170px);
    overflow-y: auto;
    padding: 20px;
}

.message-item {
    height: 100px;
    padding: 10px;
    margin-bottom: 10px;
    display: flex;
}

.user-message {
    justify-content: flex-end;
    background-color: #dcf8c6;
    margin-left: 50px;
}

.bot-message {
    justify-content: flex-start;
    background-color: #e9ecef;
    margin-right: 50px;
}


.inputbar {
    bottom: 0;
    position: absolute;
    width: calc(100% - 40px);
    margin: 20px;
}

.input-section {
    background-color: #f9f9f9;
}

.inputbar>>>.el-card__body {
    padding: 10px !important;
}

.inputbar .el-textarea>>>textarea {
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