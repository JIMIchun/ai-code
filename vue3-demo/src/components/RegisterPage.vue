<template>
    <div class="register-container">
        <el-card class="register-card">
            <h2 class="register-title">用户注册</h2>
            <el-form ref="registerFormRef" :model="registerData" :rules="registerRules" label-width="100px"
                class="register-form">
                <el-form-item label="用户名" prop="username">
                    <el-input v-model="registerData.username" placeholder="请输入用户名" clearable />
                </el-form-item>

                <el-form-item label="密码" prop="password">
                    <el-input v-model="registerData.password" placeholder="请输入密码" type="password" show-password
                        clearable />
                </el-form-item>

                <el-form-item label="确认密码" prop="confirmPassword">
                    <el-input v-model="registerData.confirmPassword" placeholder="请再次输入密码" type="password" show-password
                        clearable />
                </el-form-item>

                <el-form-item>
                    <el-button type="primary" @click="handleRegister" :loading="loading">
                        注册
                    </el-button>
                    <el-button @click="resetForm">重置</el-button>
                </el-form-item>
            </el-form>
        </el-card>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { getCurrentInstance } from 'vue';

const { proxy } = getCurrentInstance();   //获取上下文

// 表单数据
const registerData = ref({
    username: '',
    password: '',
    confirmPassword: ''
})

// 表单验证规则
const registerRules = ref({
    username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
    ],
    password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
    ],
    confirmPassword: [
        { required: true, message: '请再次输入密码', trigger: 'blur' },
        { validator: validatePassword, trigger: 'blur' }
    ]
})

// 表单引用
const registerFormRef = ref(null)
const loading = ref(false)

// 密码验证方法
function validatePassword(rule, value, callback) {
    if (value !== registerData.value.password) {
        callback(new Error('两次输入密码不一致!'))
    } else {
        callback()
    }
}

// 注册方法
const handleRegister = () => {
    registerFormRef.value.validate(async (valid) => {
        if (valid) {
            loading.value = true
            try {
                // 调用注册接口
                const response = await proxy.$axios.post('/register', {
                    username: registerData.value.username,
                    password: registerData.value.password
                })

                if (response.status === 200) {
                    ElMessage.success('注册成功！')
                    // 注册成功后的操作，例如跳转到登录页
                    // router.push('/login')
                } else {
                    ElMessage.error(response.data.message || '注册失败')
                }
            } catch (error) {
                ElMessage.error(`注册请求失败(${error.response.data.msg})`)
                console.error('注册失败:', error)
            } finally {
                loading.value = false
            }
        }
    })
}

// 重置表单
const resetForm = () => {
    registerFormRef.value.resetFields()
}

onMounted(() => {
    // 获取所有用户user
    proxy.$axios.get('/get_users').then(response => {
        console.log("all users: ", response.data)
    })
})
</script>

<style scoped>
.register-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    /* background-color: #f5f5f5; */
    
    position: relative;
    background-image: url('../assets/background-image.jpg');
    background-size: cover;
    background-position: center;
}

.register-card {
    width: 450px;
    padding: 20px;
}

.register-title {
    text-align: center;
    margin-bottom: 30px;
    color: #409eff;
}

.register-form {
    margin-top: 20px;
}

.el-button {
    width: 100px;
}
</style>