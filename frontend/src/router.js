import {createRouter, createWebHistory} from 'vue-router'
import HomePage from './components/HomePage.vue'
import CustomerLogin from "./components/CustomerLogin.vue"
import CustomerRegister from "./components/CustomerRegister.vue"
import AdminLogin from './components/AdminLogin.vue'
import CustomerHome from './components/CustomerHome.vue'
import ProfessionalRegister from './components/ProfessionalRegister.vue'
import AdminHome from './components/AdminHome.vue'
import ProLogin from './components/ProfessionalLogin.vue'
import AddService from './components/AddService.vue'

const routes=[
    {name:'HomePage', path:'/', component: HomePage},
    {name:'CustomerLogin', path:'/customer_login', component:CustomerLogin},
    {name:'CustomerRegister', path:'/customer_register', component:CustomerRegister},
    {name:'CustomerHome', path:'/customer_dashboard', component:CustomerHome},
    {name:'ProRegister', path:'/pro_register', component:ProfessionalRegister},
    {name:'ProLogin', path:'/pro_login', component:ProLogin}, 
    {name:'AddService', path:'/add_service', component:AddService},
    {name:'AdminLogin', path:'/admin_login', component:AdminLogin},
    {name:'AdminHome', path:'/admin_dashboard',component:AdminHome},
    
]

const router = createRouter({
    routes:routes,
    history:createWebHistory()
})

export default router