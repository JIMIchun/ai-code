import { createRouter, createWebHashHistory } from "vue-router";
import MainPage from '@/components/MainPage.vue'
import BlankPage from '@/components/BlankPage.vue'
import ChatPage from '@/components/ChatPage.vue'
const routes = [
    {
        path: '/',
        name: 'MainPage',
        component: MainPage,
        children: [
            {
                path: '',  // default route
                redirect: 'blank'
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
            {
                path: 'dbtest',
                name: 'DbTestPage',
                component: () => import('@/components/dbTestPage.vue')
            }
        ]
    }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes, // short for `routes: routes`
})

export default router