<template>
    <div class="login-container">
        <el-card class="login-card">
            <h2 class="login-title">用户登录</h2>
            <el-form ref="loginFormRef" :model="loginForm" :rules="loginRules" label-width="100px" class="login-form">
                <el-form-item label="用户名" prop="username">
                    <el-input v-model="loginForm.username" placeholder="请输入用户名" clearable />
                </el-form-item>

                <el-form-item label="密码" prop="password">
                    <el-input v-model="loginForm.password" placeholder="请输入密码" type="password" show-password
                        clearable />
                </el-form-item>

                <el-form-item>
                    <el-button type="primary" @click="handleLogin" :loading="loading">
                        登录
                    </el-button>
                    <el-button @click="resetForm">重置</el-button>
                </el-form-item>

                <div class="register-link">
                    <router-link to="/register">注册新用户</router-link>
                </div>
            </el-form>
        </el-card>
    </div>
</template>

<script setup>
import { getCurrentInstance, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

const { proxy } = getCurrentInstance();

// 表单数据
const loginForm = ref({
    username: '',
    password: ''
})

// 表单验证规则
const loginRules = ref({
    username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
    ],
    password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
    ]
})

// 表单引用
const loginFormRef = ref(null)
const loading = ref(false)
const router = useRouter()

// 登录方法
const handleLogin = () => {
    loginFormRef.value.validate(async (valid) => {
        if (valid) {
            loading.value = true
            try {
                // 调用登录接口
                const response = await proxy.$axios.post('/login', {
                    username: loginForm.value.username,
                    password: loginForm.value.password
                })

                if (response.status === 200) {
                    ElMessage.success('登录成功')
                    // 记录token, 写入localStorage, 在axios请求头中添加token
                    localStorage.setItem('access_token', response.data.access_token)
                    router.push('/')
                } else {
                    ElMessage.error(response.data.message || '登录失败')
                }
            } catch (error) {
                ElMessage.error('登录请求失败')
                console.error('登录失败:', error)
            } finally {
                loading.value = false
            }
        }
    })
}

// 重置表单
const resetForm = () => {
    loginFormRef.value.resetFields()
}
</script>

<style scoped>
.login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    /* background-color: #f5f5f5; */

    position: relative;
    background-image: url('../assets/background-image.jpg');
    background-size: cover;
    background-position: center;
}

.login-card {
    width: 450px;
    padding: 20px;
}

.login-title {
    text-align: center;
    margin-bottom: 30px;
    color: #409eff;
}

.login-form {
    margin-top: 20px;
}

.el-button {
    width: 100px;
}

.register-link {
    text-align: right;
    margin-top: 10px;
}
</style>