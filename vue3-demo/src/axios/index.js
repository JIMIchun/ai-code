// src/axios/index.js
import axios from 'axios';
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
        // 处理请求错误
        return Promise.reject(error);
    }
)
// instance.interceptors.response.use(...)
export default instance;
