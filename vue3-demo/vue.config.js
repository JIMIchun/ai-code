const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/api': {
        // target: 'http://192.168.1.130:5000', // 目标服务器地址
        target: 'http://localhost:5000', // 目标服务器地址
        changeOrigin: true, // 是否跨域
        pathRewrite: {
          '^/api': '' // 重写路径
        }
      }
    }
  }
})
