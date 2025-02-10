<template>
  <h2>Register as a Professional</h2>
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
      <label for="service_category"> Service Category</label>
      <select v-model="form.service_category">
        <option>Cleaning</option>
        <option>Health and Wellness</option>
        <option>Saloon</option>
        <option>Electrician</option>
        <option>Home Decoration</option>
      </select>
    </div>

    <div>
      <label for="service_name">Service Name</label>
      <select id="service_name" @change="handleSelectionChange" required>
        <option v-for="(service,index) in service_name" :key="index" >{{service}}</option>
      </select>
    </div>

    <div>
      <label for="experience">Experience</label>
      <input type="number" id="experience" v-model="form.experience">
    </div>

    <div class="form-group">
      <label for="address">Address</label>
      <input type="text" id="address" v-model="form.address" required />
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
        service_category: "",
        experience: "",
        service_name: "",
      },
      errorMessage: "",
      service_name:null
    };
  },
  methods: {
    async handleSubmit() {
      this.errorMessage = ""; 

      try {
        const response = await axios.post("http://127.0.0.1:5000/register_professional",this.form);

        if (response.status === 200) {
          alert(response.data.message);
        }

        
      } catch (error) {
        if (error.response) {
          if (error.response.status === 400 || error.response.status === 404) {
            this.errorMessage = error.response.data.message;
          }
        }
      }
    },
    async fetchData(){
      try{
      const result = await axios.get('http://127.0.0.1:5000/available_services')

      if(result.status === 200){
          this.service_name = result.data.service
          console.log(this.service_name)
      }
      }
      catch(error){
        if(error.response && (error.response.status === 400 || error.response.status === 404)){
          this.errorMessage='Some error occured'
        }
      }
    },
    handleSelectionChange(event) {
      this.form.service_name = event.target.value
    }
  },
  beforeMount(){
    this.fetchData()

  }
};
</script>

<style scoped>
form{
  width: 20%;
  margin: 0 auto;
}

form button{
  margin:0px 10px;
}
</style>