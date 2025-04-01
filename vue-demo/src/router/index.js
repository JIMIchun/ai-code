import Vue from 'vue'
import Router from 'vue-router'
import MainPage from '@/components/MainPage'
import ChatPage from '../components/ChatPage.vue'
import BlankPage from '../components/BlankPage.vue'

Vue.use(Router)

export default new Router({
  routes: [
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
        }
      ]
    }
  ]
})
