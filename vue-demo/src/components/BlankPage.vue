<template>

    <div class="content-container">
        <div class="content">
            <div class="title"><i class="el-icon-s-promotion" style="margin-right: 10px;"></i>{{ selectModel }}</div>
            <el-card shadow="never" class="input-section">
                <el-input type="textarea" autosize v-model="userInput" placeholder="Enter your question" />
                <div class="input-buttons">
                    <div class="more-options el-icon-plus button" @click="moreOptions" title="More"></div>
                    <div class="send-message el-icon-top button" @click="sendMessage" title="Send message"></div>
                </div>
            </el-card>
            <div class="suggestions">
                <p style="margin: 0; font-size: 14px; color: #c1c1c1;"><i class="el-icon-magic-stick"></i> suggested
                </p>
                <el-card class="box-card" v-for="(sugg, index) in suggList" :key="index" shadow="hover"
                    @click.native="userInput = sugg.text">
                    <div slot="header" class="clearfix">
                        <span>{{ sugg.title }}</span>
                    </div>
                    <span>{{ sugg.text }}</span>
                </el-card>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    name: 'BlankPage',
    props: ['selectModel'],
    data() {
        return {
            userInput: '',
            suggList: [
                { title: 'Help me study', text: 'Vocabulary for a college entrance exam' },
                { title: 'Explain options trading', text: "Explain options trading in simple terms if I'm familiar with buying and selling stocks." },
                { title: 'Tell me a fun fact', text: 'Tell me a random fun fact about the Roman Empire' },
            ],
        }
    },
    methods: {
        sendMessage() {
            this.$emit('send-message', { model: this.selectModel, userInput: this.userInput })
        },

        moreOptions() {
            console.log('more options');
        },
    },
    watch: {

    }
}
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
    font-size: 50px;
    text-align: center;
    margin-bottom: 20px;
    font-weight: bold;
}

.content .input-section {
    background-color: #f9f9f9;
    border-radius: 10px;
    border: none;
}

.content>>>.el-card__body {
    padding: 10px !important;
}

.content .el-textarea>>>textarea {
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

.content .suggestions .el-card>>>.el-card__header {
    padding: 0px;
    border: none;
    font-size: 17px;
    font-weight: bold;
}

.content .suggestions .el-card.el-card>>>.el-card__body {
    padding: 0px;
    border: none;
}
</style>