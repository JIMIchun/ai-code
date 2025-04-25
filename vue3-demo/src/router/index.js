import { createRouter, createWebHashHistory } from "vue-router";
import MainPage from '@/components/MainPage.vue'
import BlankPage from '@/components/BlankPage.vue'
import ChatPage from '@/components/ChatPage.vue'
import LoginPage from '@/components/LoginPage.vue'
import RegisterPage from '@/components/RegisterPage.vue'


const routes = [
    {
        path: '/',
        name: 'MainPage',
        component: MainPage,
        children: [
            {
                path: '',  // default route
                redirect: 'chat'
            },
            {
                path: 'blank',
                name: 'BlankPage',
                component: BlankPage
            },
            {
                path: 'chat',
                name: 'ChatPage',
                component: ChatPage
            },
        ]
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
    }

]

const router = createRouter({
    history: createWebHashHistory(),
    routes, // short for `routes: routes`
})

export default router