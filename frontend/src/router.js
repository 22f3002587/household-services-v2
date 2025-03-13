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
import AdminSearch from './components/AdminSearch.vue'
import ProHome from './components/ProfessionalHome.vue'
import AdminSummary from './components/AdminSummary.vue'

const routes=[
    {name:'HomePage', path:'/', component: HomePage},
    {name:'CustomerLogin', path:'/customer_login', component:CustomerLogin},
    {name:'CustomerRegister', path:'/customer_register', component:CustomerRegister},
    {name:'CustomerHome', path:'/customer_dashboard', component:CustomerHome},
    {name:'ProRegister', path:'/pro_register', component:ProfessionalRegister},
    {name:'ProLogin', path:'/pro_login', component:ProLogin},
    {name:'ProHome', path:'/pro_dashboard',component:ProHome}, 
    {name:'AddService', path:'/add_service', component:AddService},
    {name:'AdminLogin', path:'/admin_login', component:AdminLogin},
    {name:'AdminHome', path:'/admin_dashboard',component:AdminHome},
    {name:'AdminSearch', path:'/admin_search',component:AdminSearch},
    {name:'AdminSummary', path:'/admin_summary',component:AdminSummary}
    
]

const router = createRouter({
    routes:routes,
    history:createWebHistory()
})

export default router