import axios from 'axios';
import router from '@/router';

const instance = axios.create({
    baseURL: '/api',
    // timeout: 100000,   //超时时间
});
// 添加拦截器
instance.interceptors.request.use(
    config => {
        // 在发送请求之前
        // config.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        config.headers['Content-Type'] = 'application/json'
        // 添加token
        const token = localStorage.getItem('access_token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config;
    },
    error => {
        return Promise.reject(error);
    }
)
instance.interceptors.response.use(
    response => {
        return response;
    },
    error => {
        // 处理401身份验证错误
        if (error.response && error.response.status === 401) {
            console.log('响应拦截器-错误-401')
            router.push('/login')
            localStorage.removeItem('access_token')
        }
        return Promise.reject(error);
    }
)
export default instance;
