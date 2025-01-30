import {createRouter, createWebHistory} from 'vue-router'
import CustomerLogin from "./components/CustomerLogin.vue"
import CustomerRegister from "./components/CustomerRegister.vue"
import AdminLogin from './components/AdminLogin.vue'

const routes=[
    {name:'AdminLogin', path:'/admin_login', component:AdminLogin},
    {name:'CustomerLogin', path:'/customer_login', component:CustomerLogin},
    {name:'CustomerRegister', path:'/customer_register', component:CustomerRegister}
]

const router = createRouter({
    routes:routes,
    history:createWebHistory()
})

export default router