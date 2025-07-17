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
                    <div class="top-info" style="padding: 10px;">
                        <!-- 选择患者 -->
                        <el-select v-model="selectPatientId" filterable placeholder="选择账号" style="width: 100%">
                            <template #prefix>
                                <el-icon>
                                    <Search />
                                </el-icon>
                            </template>
                            <el-option v-for="item in patientsList" :key="item.patient_id"
                                :label="item.name + '(' + item.patient_id + ')'" :value="item.patient_id" />
                        </el-select>
                        <!-- 患者信息 -->
                        <el-card class="patient-info-card">
                            <div class="avatar">{{ selectPatientInfo.name?.slice(0, 1) }}</div>
                            <div class="patient-info">
                                <div class="patient-name">{{ selectPatientInfo.name }}</div>
                                <div class="lastest-case">
                                    <el-icon>
                                        <Clock />
                                    </el-icon>
                                    最近诊断：{{ casesTimeline[0]?.treatment }}
                                </div>
                            </div>
                        </el-card>
                        <el-button class="new-session-button" @click="handleNewSession">
                            <div style="display: flex; align-items: center; column-gap: 10px;">
                                <img src="../assets/new-session.png" />
                                <span>新建会话</span>
                            </div>
                        </el-button>
                    </div>
                    <el-collapse v-model="activeNames">
                        <el-collapse-item name="1" class="cases-timeline">
                            <template #title>
                                <el-icon style="font-size: 20px; margin-right: 5px;">
                                    <ChatLineSquare />
                                </el-icon>
                                会话列表
                            </template>
                            <div class="session-list">
                                <div v-if="sessionList.length === 0" class="empty-session"> 暂无会话 </div>
                                <div v-for="(session, index) in sessionList" :id="session.session_id"
                                    :class="'session-item ' + (selectSessionId === session.session_id ? 'active' : '')"
                                    :title="session.title" @click="changeCurrentSession($event, session)"
                                    @mouseenter="sessionMouseEnter" @mouseleave="sessionMouseLeave">
                                    <div class="session-title">{{ session.title }}</div>
                                    <div class="session-operator" @click.stop="clickOperator"
                                        v-click-outside="onClickOutside">
                                        <el-icon>
                                            <MoreFilled />
                                        </el-icon>
                                    </div>
                                </div>
                            </div>
                        </el-collapse-item>
                        <el-collapse-item name="2" class="cases-timeline">
                            <template #title>
                                <div class="cardcon-title">
                                    <img src="../assets/折线.png" style="margin-right: 5px;">病历时间轴
                                </div>
                            </template>
                            <el-timeline style="margin: 10px 0; padding-left: 20px;">
                                <el-timeline-item v-for="(cases, index) in casesTimeline" :key="index"
                                    :timestamp="cases.case_date" color="#30979f">
                                    {{ cases.treatment }}
                                </el-timeline-item>
                            </el-timeline>
                        </el-collapse-item>
                        <el-collapse-item name="3" class="key-quota">
                            <template #title>
                                <div class="cardcon-title">
                                    <img src="../assets/grid.png" style="margin-right: 5px;">关键指标
                                </div>
                            </template>
                            <div ref="chartRef" style="width: 100%; height: 200px;"></div>
                        </el-collapse-item>
                    </el-collapse>
                </el-card>
            </el-aside>
            <!-- 会话操作框 -->
            <el-popover ref="popoverRef" placement="bottom-end" trigger="click" virtual-triggering
                :virtual-ref="virtualRef">
                <div class="pop-content">
                    <div class="rename-session" @click="renameSession">
                        <el-icon>
                            <EditPen />
                        </el-icon>
                        <span>重命名</span>
                    </div>
                    <div class="delete-session" @click="deleteSession">
                        <el-icon>
                            <Delete />
                        </el-icon>
                        <span>删除</span>
                    </div>
                </div>
            </el-popover>
            <el-main>
                <!-- 主要内容区域 -->
                <!-- <router-view></router-view> -->
                <ChatPage :selectSessionId="selectSessionId" :selectPatientId="selectPatientId"
                    @updateSessionTitle="querysessionList">
                </ChatPage>
            </el-main>
        </el-container>
    </el-container>
</template>

<script setup>
import { ref, onMounted, watch, unref } from 'vue';
import { useRouter } from 'vue-router';
import { getCurrentInstance } from 'vue';
import * as echarts from 'echarts';
import { ElMessageBox, ElMessage, ClickOutside as vClickOutside } from 'element-plus';
import ChatPage from './ChatPage.vue';

const { proxy } = getCurrentInstance();   //获取上下文

const router = useRouter();

const userInfo = ref({});  // 用户信息
const selectPatientId = ref('');  // 选择的患者ID
const selectPatientInfo = ref({});  // 选择的患者信息
const patientsList = ref([]);  // 当前用户下所有患者列表
const accountList = ref([]);  // 所有患者数据
const sessionList = ref([]);  // 选择患者会话列表
const selectSessionId = ref(null);  // 选择的会话ID
const casesTimeline = ref([]);  // 选择患者病历时间轴
const chartRef = ref(null);   // 关键指标图表
const activeNames = ref(['1', '2', '3']);  // 侧边栏折叠面板
const popoverRef = ref();  // 会话操作弹出框
const virtualRef = ref();  // 虚拟触发器
const popVisiable = ref(false);  // 会话操作弹出框显示状态
let chart = null;

onMounted(() => {
    initData();
    chart = echarts.init(chartRef.value);

});

watch(selectPatientId, () => {
    selectPatientInfo.value = patientsList.value.find(item => item.patient_id === selectPatientId.value);
    querysessionList();
    queryPatientTimeline();
    queryPatientQuota();
});

const onClickOutside = () => {
    unref(popoverRef).popperRef?.delayHide?.()
    popVisiable.value = false;
    // const operators = document.getElementsByClassName('session-operator');
    // for (let i = 0; i < operators.length; i++) {
    //     if (operators[i].classList.contains('active')) {
    //         operators[i].classList.remove('active');
    //     }
    // }
}

const initData = async () => {
    await getUserInfo();  // 获取用户信息
    queryPatientsByUserId();
    queryAllPatientData();
}

const getUserInfo = async () => {
    try {
        const token = localStorage.getItem('access_token');
        proxy.$axios.get('/user_info').then((response) => {
            userInfo.value = response.data;
            console.log('User info:', userInfo.value);
        })
    } catch (error) {
        console.error('获取用户信息失败:', error);
        router.push('/login');
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
// 查询选择患者会话列表
const querysessionList = async (isInit = true) => {
    const patientId = selectPatientId.value;
    proxy.$axios.get(`/get_sessions/${patientId}`).then(res => {
        if (res.status === 200) {
            sessionList.value = res.data;
            if (isInit) {
                selectSessionId.value = sessionList.value[0].session_id;
            }
            console.log('Patient sessions:', res.data)
        }
    })
        .catch((err) => {
            console.log(err);
        });
}

// 新建会话
const handleNewSession = () => {
    proxy.$axios.post('/new_session', { patient_id: selectPatientId.value, title: '未命名新会话' }).then(res => {
        if (res.status === 201) {
            querysessionList();
        }
    })
}

// 切换当前会话
const changeCurrentSession = (event, session) => {
    selectSessionId.value = session.session_id;
}

// 重命名
const renameSession = () => {
    let session_div = virtualRef.value.parentElement;
    ElMessageBox.prompt('', '修改标题', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        inputValue: session_div.getElementsByClassName('session-title')[0].innerText,
        inputPattern: /^\S+$/,
        inputErrorMessage: '标题不能为空',
    })
        .then(({ value }) => {
            proxy.$axios.post('/update_session_title', { session_id: session_div.id, title: value }).then(res => {
                if (res.status === 200) {
                    console.log('修改会话标题：', value);
                    querysessionList(false);
                }
            })
        })
        .catch(() => {
            console.log('取消重命名');
        })
        .finally(() => {
            virtualRef.value.classList.remove('active');
        })
}

const deleteSession = () => {
    let session_div = virtualRef.value.parentElement;
    ElMessageBox.confirm(
        '确定要删除该会话吗?',
        '',
        {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
        }
    )
        .then(() => {
            proxy.$axios.delete('/delete_session/' + session_div.id).then(res => {
                if (res.status === 200) {
                    console.log('删除会话成功');
                    querysessionList(session_div.id == selectSessionId.value ? true : false);
                }
            })
        })
        .catch(() => {
            console.log('取消删除');
        })
        .finally(() => {
            virtualRef.value.classList.remove('active');

        })
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
    const lineColor = getComputedStyle(document.documentElement).getPropertyValue('--primary-color').trim();
    const option = {
        tooltip: {
            trigger: 'axis'
        },
        grid: {  // 控制图表与边缘的距离
            top: 40,
            bottom: 30,
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
                itemStyle: {
                    color: lineColor,  // 将折线颜色改为红色
                },
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


const sessionMouseEnter = (event) => {
    let ele = event.currentTarget.getElementsByClassName('session-operator')[0];
    ele.classList.add('active');
    if (!popVisiable.value) {  // 保持已显示的popover不动
        virtualRef.value = ele;
    }

}

const sessionMouseLeave = (event) => {
    let ele = event.currentTarget.getElementsByClassName('session-operator')[0];
    if (!popVisiable.value) {
        ele.classList.remove('active');
    }

}

const clickOperator = (event) => {
    event.currentTarget.classList.add('active');
    popVisiable.value = true;
}
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
    padding: 10px;
}

.box-card {
    height: 100%;
    border: none;
}


.el-card {
    color: var(--font-color);
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

:deep(.box-card>.el-card__body) {
    height: 100%;
    padding: 0;
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
    color: var(--primary-color);
}

:global(.main-page .button:hover) {
    /* background-color: #e1f2f5; */
    background-color: var(--button-hover-color);
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
    background-color: var(--primary-color);
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
    color: var(--primary-color);
    border-color: var(--primary-color);
    background: var(--button-hover-color);
}

.patient-info-card {
    margin: 10px 0;
    height: 100px;
}

:deep(.patient-info-card>.el-card__body) {
    height: 80px;
    display: flex;
    align-items: flex-start;
    justify-content: flex-start;
    column-gap: 10px;
    background: var(--bkg-color);
}

.el-collapse {
    height: calc(100% - 215px);
    padding: 0 10px;
    border: none;
    overflow: auto;
}

:deep(.el-collapse-item__content) {
    padding: 0;
}

:deep(.el-collapse-item>button) {
    font-size: 17px;
    border: none;
}

:deep(.el-collapse-item__wrap) {
    border: none;
}

.patient-info-card .avatar {
    width: 50px;
    height: 50px;
    background-color: var(--primary-color);
    border-radius: 10px;
    color: #ffffff;
    font-size: 40px;
    /* text-align: center; */
    font-weight: bold;
    font-style: italic;
    line-height: 50px;
    padding: 3px;
    box-sizing: border-box;
}

.patient-info-card .patient-info {
    flex: 1;
}

.patient-name {
    font-weight: bold;
    font-size: 18px;
}

.lastest-case {
    font-size: 14px;
}

.session-list {
    padding-left: 20px;
    font-size: 15px;
}

.empty-session {
    text-align: center;
    font-size: 13px;
    color: #888;
    font-style: italic;
}

.session-item.active {
    background: var(--bkg-color);
}

.session-item {
    padding: 5px 10px;
    border-radius: 5px;
    cursor: pointer;
    margin-bottom: 2px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.session-item:not(.active):hover {
    background-color: var(--button-hover-color);
}

.session-title {
    flex: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.session-operator {
    height: 20px;
    width: 20px;
    border-radius: 5px;
    text-align: center;
    color: #7f7f7f;
    display: none;
}

.session-operator.active {
    display: block;
}

.session-operator:hover {
    background: var(--button-hover-color);
}

.pop-content {
    display: flex;
    flex-direction: column;
    gap: 3px;
}

.pop-content>div {
    padding: 5px;
    border-radius: 5px;
    display: flex;
    gap: 5px;
    align-items: center;
    cursor: pointer;
}

.pop-content>div:hover {
    background: var(--button-hover-color);
}


.new-session-button {
    width: 100%;
    height: 40px;
    border-radius: 10px;
    border-color: var(--primary-color);
    color: var(--primary-color);
    font-size: 15px;
    font-weight: bold;
}

.new-session-button:hover {
    background-color: var(--button-hover-color);
    border-color: var(--button-shadow-color);
    color: var(--primary-color);
    box-shadow: 1px 1px 4px 0px var(--button-shadow-color);
}

:deep(.box-card .el-timeline-item__tail) {
    border-left: 2px solid var(--primary-color);
}




/* 滚动条样式 */
:deep(*::-webkit-scrollbar) {
    width: 5px;
}

:deep(*::-webkit-scrollbar-thumb) {
    /* background: #0c7f8acf; */
    background-color: var(--primary-color);
    border-radius: 4px;
}

:deep(*::-webkit-scrollbar-track) {
    background: transparent;
}
</style>