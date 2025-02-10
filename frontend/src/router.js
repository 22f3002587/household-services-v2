import {createRouter, createWebHistory} from 'vue-router'
import HomePage from './components/HomePage.vue'
import CustomerLogin from "./components/CustomerLogin.vue"
import CustomerRegister from "./components/CustomerRegister.vue"
import AdminLogin from './components/AdminLogin.vue'
import CustomerHome from './components/CustomerHome.vue'
import ProfessionalRegister from './components/ProfessionalRegister.vue'

const routes=[
    {name:'HomePage', path:'/', component: HomePage},
    {name:'AdminLogin', path:'/admin_login', component:AdminLogin},
    {name:'CustomerLogin', path:'/customer_login', component:CustomerLogin},
    {name:'CustomerRegister', path:'/customer_register', component:CustomerRegister},
    {name:'CustomerHome', path:'/customer_dashboard', component:CustomerHome},
    {name:'ProRegister', path:'/pro_register', component:ProfessionalRegister}
]

const router = createRouter({
    routes:routes,
    history:createWebHistory()
})

export default router