<template>
    <div class="login-form">
        <h2>Professional Login</h2>
        <form v-on:submit.prevent="handleSubmission">
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" v-model="form.email" required>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" v-model="form.password" required>
            </div>

            <div v-if="errorMessage" class="error-message"><p>{{errorMessage}}</p></div>
            <button>Login</button>
        </form>

        <div>
            <span>Don't have an account?</span>
            <router-link to="/pro_register">Register as professional</router-link>
        </div>

        <p style="color:red;">{{$route.query.message}}</p>
        
    </div>
</template>

<script>
/*eslint-disable */
import axios from 'axios'
export default{
        data(){
            return{
                form:{
                    email:'',
                    password:''
                },
                errorMessage:''

            }
        },
        methods:{
            async handleSubmission(){
                this.errorMessage=''
                try{
                    const response = await axios.post('http://127.0.0.1:5000/login_professional', this.form)

                    if(response.status === 200){
                        localStorage.setItem('authToken',response.data.token)
                        this.$router.push('/pro_dashboard')
                    }
                     
                }
                
                catch(error){
                    if(error.response){
                        if(error.response.status=== 400 || error.response.status=== 404){
                            this.errorMessage=error.response.data.message
                        }
                    }
                }
            }
        }            
    }
</script>

<style>
.login-form {
    width: 300px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
  }

.form-group{
    margin-bottom:15px;
}

input {
    width: 100%;
    padding: 8px;
    margin: 5px 0;
    border-radius: 4px;
    border: 1px solid #ccc;
  }

  button {
    width: 100%;
    padding: 10px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  .error-message {
    color: red;
    font-size: 14px;
    margin-top: 10px;
  }
</style>

