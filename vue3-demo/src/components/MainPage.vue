<template>
    <el-container class="main-page">
        <!-- 侧边栏 -->
        <el-aside class="sidebar" width="250px" v-bind="sidebarStyle">
            <div class="menu-item" v-for="(item, index) in menuButtonList" :key="index" @click="MenuClick(item)">
                <span :class="item.icon"></span>
                {{ item.title }}
            </div>
        </el-aside>
        <el-container>
            <el-header>
                <!-- 顶部导航栏 -->
                <div class="top-bar">
                    <div class="left">
                        <el-icon class="menu-icon button" @click="handleSidebarShow()">
                            <Operation />
                        </el-icon>
                    </div>
                    <div class="right">
                        <el-icon class="button" title="通知">
                            <BellFilled />
                        </el-icon>
                        <el-icon class="button">
                            <UserFilled />
                        </el-icon>
                        <el-select v-model="selectAccount" filterable placeholder="选择账号" style="width: 150px">
                            <el-option v-for="item in accountList" :key="item.patient_id" :label="item.name"
                                :value="item.patient_id" />
                        </el-select>
                    </div>
                </div>
            </el-header>
            <el-main>
                <!-- 主要内容区域 -->
                <router-view :selectModel="selectModel" @send-message="sendMessage"></router-view>
            </el-main>
        </el-container>
    </el-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { getCurrentInstance } from 'vue';
const { proxy } = getCurrentInstance();   //获取上下文

const router = useRouter();

const isShowSidebar = ref(false);
const selectModel = ref('IMRIS');
const selectAccount = ref('');
const accountList = ref([]);

// const modelList = [
//     {
//         value: 'IMRIS',
//         label: 'IMRIS医疗辅助助手'
//     }
// ];

const menuButtonList = [
    { title: 'New chat', icon: 'el-icon-edit', click: 'newChat' },
    { title: 'Workspace', icon: 'el-icon-menu', click: 'openWorkspace' },
];

onMounted(() => {
    queryAllPatientData();
});

const handleSidebarShow = () => {
    isShowSidebar.value = !isShowSidebar.value;
}
const sidebarStyle = computed(() => {
    return {
        style: {
            display: isShowSidebar.value ? 'block' : 'none'
        }
    }
});

const MenuClick = (menu) => {
    const clickFunc = menu.click;
    if (clickFunc && typeof clickFunc === 'function') {
        clickFunc();
    }
};

// const newChat = () => {
//     console.log('New chat!');
// };
// const openWorkspace = () => {
//     console.log('Open workspace!');
// };

const sendMessage = (params) => {
    console.log('Send message:', params);
    router.push({ path: '/chat', query: params });
};


// 查询所有患者数据
const queryAllPatientData = async () => {
    proxy.$axios.get('/patients').then((res) => {
        accountList.value = res.data;
        selectAccount.value = res.data[0].patient_id;
        console.log('All patient data:', accountList.value);
    })
        .catch((err) => {
            console.log(err);
        });
}

</script>

<style scoped>
.main-page {
    height: 100%;
}

.main-page .sidebar {
    display: none;
    background: #f8f8f8;
    border-radius: 0 10px 10px 0;
    padding: 10px;
}

.main-page .sidebar .menu-item {
    text-align: left;
    padding: 12px;
    border-radius: 15px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.main-page .sidebar .menu-item:hover {
    background-color: #efefef;
}

.menu-item span {
    margin-right: 10px;
}

:global(.main-page .button) {
    font-size: 18px;
    border-radius: 10px;
    padding: 10px;
    cursor: pointer;
    font-weight: bold;
    color: #7d7d7d;
}

:global(.main-page .button:hover) {
    background-color: #efefef;
}

.top-bar {
    height: 40px;
    padding: 20px 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.top-bar .left {
    display: flex;
    align-items: center;
}

.top-bar .left .menu-icon {
    margin-right: 10px;
}

.top-bar>.right {
    display: flex;
    align-items: center;
}
</style>