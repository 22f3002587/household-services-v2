<template>
<h1>Welcome to Home Assist</h1>
<button><router-link to="/customer_login">Customer Login</router-link></button> | 
<button><router-link to="/admin_login">Admin Login</router-link></button> |
<button><router-link to="/professional">Professional Login</router-link></button>

<router-view></router-view>
</template>

<script>
export default{
    name:'HomePage'
}

</script>

<style scoped>
    button{
        width:20%;
    }
</style>