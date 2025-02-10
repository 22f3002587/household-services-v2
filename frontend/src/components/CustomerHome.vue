<template>
  <div>
    <div class="navbar">
      <h1>Welcome to Customer Dashboard</h1>
      <a href="/logout_user">Logout</a>
      <a href="/customer_search">Search</a>
      <a href="#">Home</a>
    </div>
    <br />

    <div class="profile">
      <button class="prof-button" @click="toggleProfile">View Profile</button>
      <div class="dropdown-profile-content">
        <img src="/static/image.png" alt="user-image" />
        <h3>Hello, {{ userData.fullname }}</h3>
        <h3>
          Your Email: <span>{{ userData.email }}</span>
        </h3>
        <h3>Experience: {{ userData.experience }}</h3>
        <h3>Specialisation: {{ userData.specialisation }}</h3>
        <h3>Admin Approval: {{ userData.adminApproval }}</h3>
      </div>
    </div>

    <h2>Hello, {{ userData.fullname }}</h2>
    <br />

    <div class="services">
      <h3>Looking for which service category?</h3>
      <div v-for="category in categories" :key="category" class="dropdown">
        <button>{{ category }}</button>
        <div class="dropdown-content" v-if="filteredServices(category).length">
          <table>
            <tr
              v-for="service in filteredServices(category)"
              :key="service.service_id"
            >
              <td>{{ service.service_name }}</td>
              <td>{{ service.description }}</td>
              <td>Rs. {{ service.base_price }}</td>
              <td>
                <button class="btn" @click="bookService(service.service_id)">
                  Book
                </button>
              </td>
            </tr>
          </table>
        </div>
      </div>
    </div>

    <p
      v-if="alertMessage"
      style="text-align: center; font-size: 20px; color: green"
    >
      {{ alertMessage }}
    </p>

    <div class="table">
      <p style="font-size: 29px; font-family: system-ui">Requested Services:</p>
      <p v-if="!serviceRequests.length" id="no_exist">
        Your service request is empty
      </p>

      <table v-else>
        <tr>
          <th>Request ID</th>
          <th>Service Name</th>
          <th>Professional ID</th>
          <th>Request Date</th>
          <th>Scheduled Date</th>
          <th>Closed Date</th>
          <th>Status</th>
          <th>Action</th>
        </tr>
        <tr v-for="request in serviceRequests" :key="request.request_id">
          <td>{{ request.request_id }}</td>
          <td>{{ request.service_name }}</td>
          <td>{{ request.professional_id }}</td>
          <td>{{ formatDate(request.requested_date) }}</td>
          <td>{{ formatDate(request.scheduled_date) }}</td>
          <td>
            {{
              request.closed_date
                ? formatDate(request.closed_date)
                : "Closing Date Pending"
            }}
          </td>
          <td>{{ request.status }}</td>
          <td>
            <button
              v-if="request.status === 'Requested'"
              class="close"
              @click="closeRequest(request.request_id)"
            >
              Close
            </button>
            <button
              v-if="request.status === 'Requested'"
              class="edit close"
              @click="editRequest(request.request_id)"
            >
              Edit
            </button>
            <button
              v-if="
                ['Requested', 'Closed by customer'].includes(request.status)
              "
              style="background-color: orangered"
              class="close"
              @click="deleteRequest(request.request_id)"
            >
              Delete
            </button>
          </td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      userData: {
        fullname: '',
        email: '',
        experience: '',
        specialisation: '',
        adminApproval: '',
      },
      services: [
        { service_id: 1, service_name: 'House Cleaning', description: 'Thorough cleaning', base_price: 1500, service_category: 'Cleaning' },
        { service_id: 2, service_name: 'Hair Styling', description: 'Trendy styles', base_price: 800, service_category: 'Saloon' },
        // Add more services as needed
      ],
      categories: ['Cleaning', 'Home Decoration', 'Health & Wellness', 'Saloon', 'Electrician'],
      serviceRequests: [
        { request_id: 101, service_name: 'House Cleaning', professional_id: 'PRO123', requested_date: '2024-10-01', scheduled_date: '2024-10-05', closed_date: null, status: 'Requested' },
        // Add more requests as needed
      ],
      alertMessage: '',
      showProfile: false,
    };
  },
  methods: {
    toggleProfile() {
      this.showProfile = !this.showProfile;
    },
    filteredServices(category) {
      return this.services.filter(service => service.service_category === category);
    },
    bookService(serviceId) {
      this.alertMessage = `Service with ID ${serviceId} booked successfully!`;
    },
    closeRequest(requestId) {
      this.alertMessage = `Request ${requestId} has been closed.`;
    },
    editRequest(requestId) {
      this.alertMessage = `Editing request ${requestId}.`;
    },
    deleteRequest(requestId) {
      this.alertMessage = `Request ${requestId} has been deleted.`;
      this.serviceRequests = this.serviceRequests.filter(req => req.request_id !== requestId);
    },
    formatDate(date) {
      const d = new Date(date);
      return `${d.getDate().toString().padStart(2, '0')}-${(d.getMonth() + 1).toString().padStart(2, '0')}-${d.getFullYear()}`;

    },
    async fetchuserData(){
      const token= localStorage.getItem('authToken')
      try{
        const response = await axios.get('http://localhost:5000/customer/dashboard',{headers:{
          Authorization:token
        }
        })

        if(response.status===200){
          console.log("fetching data....")
        }
      }
      catch(error){
        if(error.response){
          alert('Something went wrong')
        }
      }
    }
  },
  mounted(){
    this.fetchuserData()
  }
}        
</script>

<style scoped>
body {
  display: flex;
  flex-direction: column;
}

.navbar {
  background-color: black;
  color: white;
  margin-top: -5px;
}

h3 {
  position: absolute;
  margin: 118px;
  font-size: 24px;
}

.navbar a {
  font-size: 19px;
  float: right;
  display: block;
  padding: 0px 16px;
  text-decoration: none;
  color: azure;
  margin-top: -13px;
  margin-bottom: 28px;
}

h1 {
  font-size: xx-large;
  font-weight: bolder;
  margin-bottom: -35px;
  padding: 20px;
  margin-top: 2px;
  font-family: Cambria, Cochin, Georgia, Times, "Times New Roman", serif;
}

h2 {
  margin: 16px;
  margin-top: -23px;
  padding: 12px;
  text-align: center;
  font-size: 34px;
}

.table {
  margin: 23px 111px;
}

.services {
  margin: 0 auto;
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  border: 2px solid white;
  border-radius: 13px;
  width: 68%;
  height: 175px;
  background-color: cornsilk;
}

.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: white;
  width: 350px;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  z-index: 1;
  padding: 10px;
  top: 100%;
  left: -40%;
}

.dropdown:hover .dropdown-content {
  display: block;
}

button {
  padding: 10px;
  cursor: pointer;
  margin-bottom: 19px;
  height: 64px;
  width: 130px;
  border: 3px solid blue;
  background-color: rgb(20, 228, 228);
  border-radius: 12px;
  font-size: 16px;
}

button:hover {
  background-color: #afdd5f;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  border: 1px solid black;
  padding: 8px;
  text-align: left;
}

.btn {
  width: 108%;
  height: 41px;
  font-size: 90%;
  background-color: white;
}

.profile {
  position: relative;
  display: inline-block;
  left: 53%;
  margin-top: 27px;
}

.dropdown-profile-content {
  display: none;
  position: absolute;
  background-color: antiquewhite;
  width: 295px;
  box-shadow: 0px 8px 16px 0px black;
  z-index: 1;
  padding: 10px;
  top: 100%;
  left: 50%;
  transform: translate(-50%);
  border-radius: 5px;
}

.prof-button {
  background-color: green;
  color: white;
  padding: 10px 20px;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  width: 125px;
  height: 37px;
}

.prof-button:hover {
  background-color: darkgreen;
}

img {
  width: 90px;
  margin: 0px 100px;
  margin-bottom: -15px;
}

.close {
  background-color: black;
  color: white;
  width: 85px;
  height: 35px;
  font-size: 15px;
  border: none;
}

.close:hover {
  background-color: paleturquoise;
  color: black;
}

.edit {
  background-color: lightgreen;
  border: lightgreen;
  width: 106px;
}
</style>
