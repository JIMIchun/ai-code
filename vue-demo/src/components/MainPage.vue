<template>
  <el-container class="main-page">
    <!-- 侧边栏 -->
    <el-aside class="sidebar" width="250px" ref="sidebar">
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
            <div class="menu-icon el-icon-s-operation button" title="Menu" @click="handleSidebarShow()"></div>
            <template>
              <el-select v-model="selectModel" filterable placeholder="Select a model">
                <el-option v-for="item in modelList" :key="item.value" :label="item.label" :value="item.value">
                </el-option>
              </el-select>
            </template>
          </div>
          <div class="right">
            <div class="el-icon-edit button" title="New chat" @click="newChat()"></div>
            <div class="el-icon-bell button" title="Settings"></div>
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

<script>

export default {
  name: 'MainPage',
  data() {
    return {
      modelList: [
        {
          value: 'Model1',
          label: 'Model1'
        },
        {
          value: 'Model2',
          label: 'Model2'
        },
      ],
      isShowSidebar: false,
      menuButtonList: [
        { title: 'New chat', icon: 'el-icon-edit', click: 'newChat' },
        { title: 'Workspace', icon: 'el-icon-menu', click: 'openWorkspace' },
      ],
      selectModel: 'Model1',
    };
  },
  methods: {
    handleSidebarShow() {
      this.isShowSidebar = !this.isShowSidebar;
      this.$refs.sidebar.$el.style.display = this.isShowSidebar ? 'block' : 'none';
    },

    MenuClick(menu) {
      let clickFunc = menu.click;
      if (clickFunc && typeof this[clickFunc] === 'function') {
        this[clickFunc]();
      }
    },

    newChat() {
      console.log('New chat!')
    },

    openWorkspace() {
      console.log('Open workspace!')
    },

    sendMessage(params) {
      console.log('Send message:', params);
      this.$router.push({ path: '/chat', query: params })
    },
  }
};
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

.main-page>>>.button {
  border-radius: 10px;
  padding: 10px;
  cursor: pointer;
  font-size: 17px;
  font-weight: bold;
  color: #7d7d7d;
}

.main-page>>>.button:hover {
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
</style>