<template>
    <div>
      <nav class="navbar">
        <h1>Customer Dashboard</h1>
        <div>
          <router-link :to="{ name: 'CustomerHome' }">Home</router-link>
          <router-link :to="{ name: 'HomePage' }" @click="logoutuser">Logout</router-link>
        </div>
      </nav>
  
      <div class="content">
        <h3>Search for a service</h3>
        <form @submit.prevent="searchServices">
          <label for="search_type">Search By: </label>
          <select v-model="searchType" required>
            <option value="">Select</option>
            <option value="service_name">Service Name</option>
            <option value="service_category">Service Category</option>
          </select>
          <input type="text" v-model="searchQuery" placeholder="Enter service..." required>
        </form>
  
        <table v-if="filteredServices.length">
          <thead>
            <tr>
              <th>Service Category</th>
              <th>Service Name</th>
              <th>Rating</th>
              <th>Description</th>
              <th>Price</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="record in filteredServices" :key="record.service_id">
              <td>{{ record.service_category }}</td>
              <td>{{ record.service_name }}</td>
              <td>{{ record.rating }} of 5</td>
              <td>{{ record.description }}</td>
              <td>Rs. {{ record.base_price }}</td>
              <td>
                <button class="btn" @click="bookService(record)">Book</button>
              </td>
            </tr>
          </tbody>
        </table>
        <p v-if="filteredServices.length === 0">No services found.</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        searchType: "",
        searchQuery: "",
        services: [],
      };
    },
    computed: {
      filteredServices() {
  
        return this.services.filter((service) => {
          const query = this.searchQuery.toLowerCase();
          if (this.searchType === 'service_name') {
            return service.service_name.toLowerCase().includes(query);
          } else if (this.searchType === 'service_category') {
            return service.service_category.toLowerCase().includes(query);
          }
          return true;
        });
      },
    },
    methods: {
      logoutuser() {
        localStorage.removeItem('authToken');
      },

      async bookService(record){
        try{
          const response = await axios.post('http://localhost:5000/request_service', {"service_id":record.service_id, "service_name":record.service_name}, {
            headers:{
              Authorization:`${localStorage.getItem('authToken')}`
            }
          })
          if(response.status === 200){
            this.$router.push({name:'CustomerHome', query:{"message":"Requested succesfully. Please wait for Professional response"}})
          }
        }catch(error){
          console.log(error)
        }
      }
    },
    async mounted() {
      try {
        const response = await axios.get('http://localhost:5000/search_services', {
          headers: {
            Authorization: `${localStorage.getItem('authToken')}`,
          },
        });
        if (response.status === 200) {
          this.services = response.data.services;
        }
      } catch (error) {
        if (error.response.status === 401) {
          this.$router.push({ name: 'CustomerLogin', query: { message: 'You need to login first' } });
        }
      }
    },
  };
  </script>
  
  <style scoped>
  body {
    font-family: 'Arial', sans-serif;
    background-color: #f4f4f4;
    color: #333;
    margin: 0;
    padding: 0;
  }
  
  .navbar {
    background-color: #333;
    color: white;
    padding: 10px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top:-60px;
  }
  
  .navbar a {
    color: white;
    text-decoration: none;
    padding: 10px 20px;
    transition: background 0.3s;
  }
  
  .navbar a:hover {
    background-color: #575757;
    border-radius: 5px;
  }
  
  .content {
    max-width: 900px;
    margin: 30px auto;
    padding: 20px;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  h3 {
    text-align: center;
    font-size: 22px;
    margin-bottom: 30px;
  }
  
  form {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 40px;
  }
  
  select, input[type="text"], button {
    padding: 10px;
    margin: 0 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 16px;
    width:20%;
  }
  
  select {
    width: 160px;
  }
  
  button {
    background-color: #333;
    color: white;
    cursor: pointer;
    transition: background 0.3s;
  }
  
  button:hover {
    background-color: #575757;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
  }
  
  th, td {
    padding: 12px 15px;
    text-align: left;
    border-bottom: 1px solid #ddd;
  }
  
  th {
    background-color: #333;
    color: white;
  }
  
  td {
    background-color: #f9f9f9;
  }
  
  .btn {
    padding: 8px 12px;
    background-color: #333;
    color: white;
    border: none;
    cursor: pointer;
    border-radius: 5px;
    width:auto;
  }
  
  .btn:hover {
    background-color: #575757;
  }
  </style>
  