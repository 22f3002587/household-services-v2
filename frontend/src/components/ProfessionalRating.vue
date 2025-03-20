<template>
    <div class="rating-container">
      <h2>Service Remarks</h2>
      
      <div class="content">
        <div>Name: {{ pro.fullname }}</div>
        <div>Email Id: {{ pro.email }}</div>
        <div>Service Name: {{ pro.service_name }}</div>
        <div>Experience: {{ pro.experience }} Years</div>
      </div>
  
      <form @submit.prevent="submitReview(pro.service_name)">
        <h4>Rate Service: </h4>
        
        <label for="exc"> Excellent</label>
          <input type="radio" v-model="rating" value="5" required id="exc" />
         
        <label for="good">Good</label>
          <input type="radio" v-model="rating" value="4" required id="good"/>

        <label for="avg"> Average</label>
          <input type="radio" v-model="rating" value="3" required id="avg"/>
         
        <label for="bad">Bad</label>
          <input type="radio" v-model="rating" value="2" required id="bad"/>
          
        <label for="wrst">Worst</label>
          <input type="radio" v-model="rating" value="1" required id="wrst"/>
          
        
        <button type="submit" :disabled="rating === null">Submit</button>
      </form>
    </div>
  </template>
  
  <script>
import axios from 'axios';

  export default {
    data() {
      return {
        pro: {
          fullname: '',
          email: '', 
          service_name: '', 
          experience: null, 
        },
        rating: null,  
      };
    },
    methods: {
      async submitReview(service_name) {
        try{
          const response = await axios.post(`/pro_remarks/${service_name}`,{"rating":this.rating},{
            headers:{
              Authorization:`${localStorage.getItem('authToken')}`
            }
          })
          if(response.status === 200){
            console.log('Added successfully')
            this.review = '';
            this.$router.push({name:'CustomerHome', query:{"message":"You rating has been marked"}})
          }
        }
        catch(error){
          if(error.response.status === 401){
            this.$router.push({name:'CustomerLogin', query:{"message":"You need to login first"}})
          }
        } 
      },
    },

    async mounted(){
      let service_name = this.$route.query.service_name
      try{
      const response = await axios.get(`http://localhost:5000/pro_remarks/${service_name}`,{
        headers:{
          Authorization:`${localStorage.getItem('authToken')}`
        }
      })
      if(response.status === 200){
        this.pro.fullname = response.data.pro_name
        this.pro.email = response.data.pro_email
        this.pro.experience = response.data.experience
        this.pro.service_name = response.data.service_name
      }
      }
      catch(error){
        console.log(error.response)
      }
    }
  };
  </script>
  
  <style scoped>
  .rating-container {
    max-width: 600px;
    margin: auto;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 20px;
    text-align: center;
  }
  
  h2 {
    color: #333;
  }
  
  .content {
    display: flex;
    justify-content: space-between;
    margin: 20px 0;
  }
  
  .content div {
    flex: 1;
    padding: 10px;
    border-right: 1px solid #ddd;
    height: 35px;
    text-align: center;
  }
  
  .content div:last-child {
    border-right: none;
  }
  
  label {
    margin-right: 10px;
  }
  
  textarea {
    width: 96%;
    height: 100px;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 10px;
    resize: none;
    margin-top: 10px;
    margin-bottom: 20px;
  }
  
  button {
    margin-top: 30px;
    background-color: #28a745;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 10px 20px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  button:hover {
    background-color: #218838;
  }
  
  button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
  </style>
  