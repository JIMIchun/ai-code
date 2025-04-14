<template>
    <div>
        <el-button @click="queryAllPatientData">查询所有患者数据</el-button>
    </div>
</template>

<script setup>
import { getCurrentInstance } from 'vue';
const { proxy } = getCurrentInstance();   //获取上下文

// 查询所有患者数据
const queryAllPatientData = async () => {
    proxy.$axios.get('/patients').then((res) => {
        console.log(res.data);
    })
    .catch((err) => {   
        console.log(err);
    });
}

</script>

<style scoped></style>