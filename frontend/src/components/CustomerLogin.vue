<template>
  <div class="login-container">
    <h2>Customer Login</h2>
    <form @submit.prevent="loginCustomer">
      <div>
        <label for="email">Email:</label>
        <input type="email" v-model="form.email" id="email" placeholder="Enter your email" required/>
      </div>

      <div>
        <label for="password">Password:</label>
        <input
          type="password"
          v-model="form.password"
          id="password"
          placeholder="Enter your password"
          required
        />
      </div>

      <button type="submit">Login</button>

      <div v-if="this.$route.query.message" class="error-message">
        <p>{{ this.$route.query.message }}</p>
      </div>

      <div v-if="errorMessage" class="error-message">
        <p>{{ errorMessage }}</p>
      </div>
    </form>

    <div class="register-container">
      <span>Don't have an account?</span>
      <router-link to="/customer_register">Register</router-link>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      form: {
        email: "",
        password: "",
      },
      errorMessage: "",
    };
  },
  methods: {
    async loginCustomer() {
      try {
        const response = await axios.post("http://127.0.0.1:5000/login_customer",this.form);

        if (response.status === 200) {
          localStorage.setItem("authToken", response.data.token);
          this.$router.push({name:"CustomerHome"})
        }

      } catch (error) {
        if (error.response){ 

          if (error.response.status === 400 || error.response.status === 404) {
            this.errorMessage = error.response.data.message;
          }

        }
      }
    }
  }
};
</script>

<style scoped>
.login-container {
  max-width: 378px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
}

div {
  margin-bottom: 15px;
}

input {
  width: 84%;
  padding: 10px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  width: 84%;
  padding: 10px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

.error-message {
  color: red;
  font-size: 14px;
  text-align: center;
}

.register-container {
  text-align: center;
  margin-top: 15px;
}

.register-container span {
  margin-right: 5px;
}

.register-container router-link {
  font-weight: bold;
  color: #4caf50;
}

.register-container router-link:hover {
  color: #45a049;
}
</style>
