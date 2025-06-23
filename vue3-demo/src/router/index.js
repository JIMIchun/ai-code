import { createRouter, createWebHashHistory } from "vue-router";
import MainPage from '@/components/MainPage.vue'
import BlankPage from '@/components/BlankPage.vue'
import ChatPage from '@/components/ChatPage.vue'
import LoginPage from '@/components/LoginPage.vue'
import RegisterPage from '@/components/RegisterPage.vue'


const routes = [
    {
        path: '/',
        redirect: '/main'
    },
    {
        path: '/main',
        name: 'MainPage',
        component: MainPage
    },
    {
        path: '/login',
        name: 'LoginPage',
        component: LoginPage
    },
    {
        path: '/register',
        name: 'RegisterPage',
        component: RegisterPage
    },

    {
        path: '/test',
        name: 'testPage',
        component: () => import('@/components/voice-test.vue')
    }

]

const router = createRouter({
    history: createWebHashHistory(),
    routes, // short for `routes: routes`
})

export default router