<template>
    <el-container class="main-page">
        <el-header>
            <!-- 顶部导航栏 -->
            <div class="top-bar">
                <div class="left">
                    <div class="doc-image">
                        <img src="../assets/doctor.svg">
                    </div>
                    <div class="bar-title" style="margin-left: 10px; text-align: left;">
                        <div style="color: #FFFFFF; font-weight: bold; font-size: 18px;">IMRIS医疗辅助中心</div>
                        <div style=" color: #dedede; font-size: 13px;">医疗AI智能诊疗平台</div>
                    </div>
                </div>
                <div class="right">
                    <el-icon class="button" title="通知">
                        <BellFilled />
                    </el-icon>
                    <el-icon class="button">
                        <UserFilled />
                    </el-icon>
                    <!-- 选择患者 -->
                    <el-select v-model="selectAccount" filterable placeholder="选择账号" style="width: 150px">
                        <el-option v-for="item in accountList" :key="item.patient_id" :label="item.name"
                            :value="item.patient_id" />
                    </el-select>
                </div>
            </div>
        </el-header>
        <el-container style="height: calc(100% - 60px);">
            <el-aside class="sidebar" width="250px">
                <el-card class="box-card">
                    <template #header> 病情概览 </template>
                    <div class="cases-timeline">
                        <div class="cardcon-title">
                            <img src="../assets/折线.png" style="margin-right: 5px;">病历时间轴
                        </div>
                        <el-timeline style="margin: 10px 0; padding-left: 20px;">
                            <el-timeline-item v-for="(cases, index) in casesTimeline" :key="index"
                                :timestamp="cases.case_date">
                                {{ cases.treatment }}
                            </el-timeline-item>
                        </el-timeline>
                    </div>
                    <div class="key-quota">
                        <div class="cardcon-title">
                            <img src="../assets/grid.png" style="margin-right: 5px;">关键指标
                        </div>
                        <div ref="chartRef" style="width: 100%; height: 200px;"></div>
                    </div>
                </el-card>
            </el-aside>
            <el-main>
                <!-- 主要内容区域 -->
                <router-view @send-message="sendMessage"></router-view>
            </el-main>
        </el-container>
    </el-container>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { getCurrentInstance } from 'vue';
import * as echarts from 'echarts';

const { proxy } = getCurrentInstance();   //获取上下文

const router = useRouter();

// const isShowSidebar = ref(false);
const selectAccount = ref('');
const accountList = ref([]);
const casesTimeline = ref([]);
const chartRef = ref(null);


onMounted(() => {
    queryAllPatientData();
    initChart();
});

watch(selectAccount, () => {
    queryPatientTimeline();
});

const sendMessage = (params) => {
    console.log('Send message:', params);
    router.push({ path: '/chat', query: params });
};


// 查询所有患者数据
const queryAllPatientData = async () => {
    proxy.$axios.get('/patients').then((res) => {
        accountList.value = res.data;
        selectAccount.value = res.data[0].patient_id;
        queryPatientTimeline();
        console.log('All patient data:', accountList.value);
    })
        .catch((err) => {
            console.log(err);
        });
}

// 查询患者病历时间轴
const queryPatientTimeline = async () => {
    const patientId = selectAccount.value;
    proxy.$axios.get('/cases_by_patient/' + patientId).then((res) => {
        casesTimeline.value = res.data;
        console.log('Patient timeline:', casesTimeline.value);
    })
        .catch((err) => {
            console.log(err);
        });
}

const initChart = () => {
    const chart = echarts.init(chartRef.value);
    const option = {
        tooltip: {
            trigger: 'axis'
        },
        xAxis: {
            type: 'category',
            data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                data: [1, 2, 4, 2, 3, 5, 1],
                type: 'line'
            }
        ]
    };
    chart.setOption(option);
}

</script>

<style scoped>
.main-page {
    height: 100%;
    position: relative; /* 添加定位属性以便伪元素可以相对于其进行定位 */
    background-image: url('../assets/background-image.jpg');
    background-size: cover; /* 使背景图片覆盖整个元素 */
    background-position: center; /* 使背景图片居中 */
}

.main-page::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.9) 0%, rgba(255, 255, 255, 0) 100%);
    z-index: 0; 
}
.main-page>*{
    z-index: 1;
}

.main-page .sidebar {
    /* background: #f8f8f8;
    border-radius: 0 10px 10px 0; */
    padding: 10px;
}

.el-card {
    color: #1A2B3C;
    text-align: left;
}

:deep(.sidebar .el-card__header) {
    padding: 5px;
    text-align: left;
    border: none;
    font-weight: bold;
}

:deep(.sidebar .el-card__body) {
    padding: 10px;
}

.sidebar .cardcon-title {
    display: flex;
    align-items: center;
}

:global(.main-page .button) {
    font-size: 18px;
    border-radius: 10px;
    padding: 10px;
    cursor: pointer;
    font-weight: bold;
    color: #f9f9f9;
}

:global(.main-page .button:hover) {
    /* background-color: #efefef; */
    background-color: #48758d;
}

header.el-header {
    border-bottom: 1px solid #bdbdbd;
}

.top-bar {
    padding: 10px 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.top-bar .left {
    display: flex;
    align-items: center;
}

.doc-image {
    background-color: #2A5C82;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: space-around;
}

.top-bar>.right {
    display: flex;
    align-items: center;
}
/* 滚动条样式 */
:deep(*::-webkit-scrollbar) {
    width: 4px;
}
:deep(*::-webkit-scrollbar-thumb) {
    background: #ffffff;
    border-radius: 4px;
}
:deep(*::-webkit-scrollbar-track) {
    background: transparent;
}
</style>