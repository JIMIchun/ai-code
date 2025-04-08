// src/axios/index.js
import axios from 'axios';
const instance = axios.create({
    baseURL: '/api',
    // timeout: 100000,   //超时时间
});
// 添加拦截器
instance.interceptors.request.use(
    config => {
        // 在发送请求之前做些什么
        config.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        return config;
    },
    error => {
        // 对请求错误做些什么
        return Promise.reject(error);
    }
)
// instance.interceptors.response.use(...)
export default instance;
