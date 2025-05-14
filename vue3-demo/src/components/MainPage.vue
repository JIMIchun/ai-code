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
                        <div style=" color: #f9f9f9; font-size: 13px;">医疗AI智能诊疗平台</div>
                    </div>
                </div>
                <div class="right">
                    <el-icon class="button" title="通知">
                        <BellFilled />
                    </el-icon>
                    <el-popover placement="bottom" trigger="hover" width="200">
                        <template #reference>
                            <el-icon class="button">
                                <UserFilled />
                            </el-icon>
                        </template>
                        <div class="user-info-card">
                            <div class="user-details">
                                <div class="username">用户名：{{ userInfo.username }}</div>
                                <div class="user-role">职称：主治医师</div>
                            </div>
                            <el-button plain size="small" @click="handleLogout" style="margin-top: 10px; width: 100%">
                                退出登录
                            </el-button>
                        </div>
                    </el-popover>

                    <!-- <img src="../assets/exit.svg" class="button" title="退出登录" @click="handleLogout" /> -->
                </div>
            </div>
        </el-header>
        <el-container style="height: calc(100% - 60px);">
            <!-- 侧边栏 -->
            <el-aside class="sidebar" width="300px">
                <el-card class="box-card">
                    <!-- 选择患者 -->
                    <el-select v-model="selectPatientId" filterable placeholder="选择账号" style="width: 100%">
                        <template #prefix>
                            <el-icon>
                                <Search />
                            </el-icon>
                        </template>
                        <el-option v-for="item in patientsList" :key="item.patient_id" :label="item.name"
                            :value="item.patient_id" />
                    </el-select>
                    <el-card class="patient-info-card">
                        <div class="avatar">{{ selectPatientInfo.name?.slice(0,1)  }}</div>
                        <div class="patient-info">
                            <div class="patient-name">{{ selectPatientInfo.name}}</div>
                        </div>

                    </el-card>
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
import { ElMessageBox } from 'element-plus';

const { proxy } = getCurrentInstance();   //获取上下文

const router = useRouter();

// const isShowSidebar = ref(false);
const userInfo = ref({});
const selectPatientId = ref('');
const selectPatientInfo = ref({});
const patientsList = ref([]);
const accountList = ref([]);
const casesTimeline = ref([]);
const chartRef = ref(null);
let chart = null;

onMounted(() => {
    initData();
    chart = echarts.init(chartRef.value);

});

watch(selectPatientId, () => {
    selectPatientInfo.value = patientsList.value.find(item => item.patient_id === selectPatientId.value);
    queryPatientTimeline();
    queryPatientQuota();
});

const initData = async () => {
    await getUserInfo();  // 获取用户信息
    queryPatientsByUserId();
    queryAllPatientData();
}


const sendMessage = (params) => {
    console.log('Send message:', params);
    router.push({ path: '/chat', query: params });
};

const getUserInfo = async () => {
    try {
        const token = localStorage.getItem('access_token');
        proxy.$axios.get('/user_info').then((response) => {
            userInfo.value = response.data;
            console.log('User info:', userInfo.value);
        })
    } catch (error) {
        console.error('获取用户信息失败:', error);
    }
}

const queryPatientsByUserId = async () => {
    proxy.$axios.get('/get_patients_by_user').then((res) => {
        patientsList.value = res.data;
        console.log(`user ${userInfo.value.username}'s patients data:`, patientsList.value);
    })
}

// 查询所有患者数据
const queryAllPatientData = async () => {
    proxy.$axios.get('/patients').then((res) => {
        accountList.value = res.data;
        selectPatientId.value = res.data[0].patient_id;
        console.log('All patient data:', accountList.value);
    })
        .catch((err) => {
            console.log(err);
        });
}

// 查询患者病历时间轴
const queryPatientTimeline = async () => {
    const patientId = selectPatientId.value;
    proxy.$axios.get('/cases_by_patient/' + patientId).then((res) => {
        casesTimeline.value = res.data;
        console.log('Patient timeline:', casesTimeline.value);
    })
        .catch((err) => {
            console.log(err);
        });
}

// 查询患者关键指标
const queryPatientQuota = async () => {
    const patientId = selectPatientId.value;
    proxy.$axios.get('/cea_level/' + patientId).then((res) => {
        console.log('Patient quota:', res.data);
        initChart(res.data); // 更新图表
    })
        .catch((err) => {
            console.log(err);
        });
}

/**
 * @description 初始化图表
 * @param quatoData [] 关键指标数据列表
 */
const initChart = (quatoData) => {
    const option = {
        tooltip: {
            trigger: 'axis'
        },
        grid: {  // 控制图表与边缘的距离
            top: 50,
            bottom: 40,
            left: 30,
            right: 40
        },
        xAxis: {
            type: 'category',
            data: quatoData.map(item => item.time_point),
            name: '(周)',
            axisTick: {
                show: true,
                alignWithLabel: true
            }
        },
        yAxis: {
            type: 'value',
            show: true,
            name: "CEA 水平(ng/mL)",
            nameLocation: "end",
            nameTextStyle: {
                align: "left",
                overflow: "break",
                width: 10
            },
        },
        series: [
            {
                data: quatoData.map(item => Number(item.ceal_level)),
                type: 'line',
                label: {
                    show: true,
                    position: "bottom"
                }
            }
        ]
    };
    chart.setOption(option);
}

/**
 * @description 退出登录方法
 */
const handleLogout = () => {
    ElMessageBox.confirm('确定要退出登录吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
    }).then(() => {
        // 清除token
        localStorage.removeItem('access_token');
        // 跳转到登录页
        router.push('/login');
    }).catch(() => {
        // 用户取消操作
    });
};


</script>

<style scoped>
.main-page {
    height: 100%;
    position: relative;
    background-image: url('../assets/background-image.jpg');
    background-size: cover;
    background-position: center;
}

.main-page::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.85) 0%, rgba(255, 255, 255, 0.4) 50%, rgba(255, 255, 255, 0.1) 100%);
    z-index: 0;
}

.main-page>* {
    z-index: 1;
}

.main-page .sidebar {
    /* background: #f8f8f8;
    border-radius: 0 10px 10px 0; */
    padding: 10px;
}

.box-card {
    height: 100%;
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
    color: #0097A7;
}

:global(.main-page .button:hover) {
    /* background-color: #efefef; */
    background-color: #e1f2f5;
}

header.el-header {
    border-bottom: 1px solid #ffffff;
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
    /* background-color: #79c1cf; */
    background-color: #0097A7;
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

.user-info-card .el-button:hover {
    color: #0097A7;
    border-color: #0097A7;
    background: #0097a71a;
}

.patient-info-card {
    margin: 10px 0;
    height: 100px;
}
:deep(.patient-info-card>.el-card__body){
    height: 80px;
    display: flex;
    align-items: flex-start;
    justify-content: flex-start;
    column-gap: 10px;
}

.patient-info-card .avatar{
    width: 50px;
    height: 50px;
    background-color: #0097A7;
    border-radius: 10px;
    color: #ffffff;
    font-size: 40px;
    text-align: center;
    font-weight: bold;
    font-style: italic;
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