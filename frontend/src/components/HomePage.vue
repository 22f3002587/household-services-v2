<template>
<h1>Welcome to Home Assist</h1>
<router-link to="/customer_login">Customer Login</router-link> | 
<router-link to="/admin_login">Admin Login</router-link> |
<router-link to="/professional">Professional Login</router-link>

<router-view></router-view>
</template>

<script>
export default{
    name:'HomePage'
}

</script>