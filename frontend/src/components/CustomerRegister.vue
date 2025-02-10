<template>
  <div class="registration-form">
    <h2>Register as a Customer</h2>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="fullname">Full Name</label>
        <input type="text" id="fullname" v-model="form.fullname" required />
      </div>

      <div class="form-group">
        <label for="email">Email</label>
        <input type="email" id="email" v-model="form.email" required />
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" v-model="form.password" required />
      </div>

      <div class="form-group">
        <label for="address">Address</label>
        <input type="text" id="address" v-model="form.address" required />
      </div>

      <div class="form-group">
        <label for="contact">Contact Number</label>
        <input type="text" id="contact" v-model="form.contact" required />
      </div>

      <div class="form-group">
        <label for="pincode">Pincode</label>
        <input type="text" id="pincode" v-model="form.pincode" required />
      </div>

      <div v-if="errorMessage" class="error-message">
        <p>{{ errorMessage }}</p>
      </div>

      <button>Register</button>
    </form>

    <router-link to="/customer_login">Login</router-link>
    <router-view></router-view>
  </div>
</template>

<script>
/* eslint-disable */
import axios from "axios";

export default {
  data() {
    return {
      form: {
        fullname: "",
        email: "",
        password: "",
        address: "",
        contact: "",
        pincode: "",
      },
      errorMessage: "",
    };
  },
  methods: {
    async handleSubmit() {
      this.errorMessage = ""; // Reset error message on each submit

      try {
        const response = await axios.post("http://127.0.0.1:5000/register_customer",this.form);

        if (response.status === 200) {
          alert(response.data.message);

        }

      } catch (error) {
        if(error.response){

          if(error.response.status === 400 || error.response.status === 404){
            this.errorMessage=error.response.data.message
          }
        }
      }
    }
  }
};
</script>

<style scoped>
.registration-form {
  width: 300px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.form-group {
  margin-bottom: 15px;
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
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background-color: #ccc;
}

.error-message {
  color: red;
  font-size: 14px;
  margin-top: 10px;
}
</style>
