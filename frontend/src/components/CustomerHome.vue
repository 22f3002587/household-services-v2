<template>
  <div class="customer-dashboard">
    <div class="navbar">
      <h1>Welcome to Customer Dashboard</h1>
      <div class="nav-links">
        <router-link :to="{ name: 'HomePage' }" @click="logoutuser">Logout</router-link>
        <a href="/customer_search">Search</a>
        <a href="#">Home</a>
      </div>
    </div>

    <div class="profile">
      <button class="prof-button" style="background-color:black;" @click="toggleProfileDropdown">View
        Profile</button><br><br>
      <div v-if="isProfileDropdownVisible" class="dropdown-profile-content">
        <img style="width:100px; border-radius:116px;"
          src="https://img.freepik.com/premium-vector/silver-membership-icon-default-avatar-profile-icon-membership-icon-social-media-user-image-vector-illustration_561158-4195.jpg?semt=ais_hybrid"
          alt="user-image">
        <h3>Hello {{ profile.name }}</h3>
        <table class="profile-table">
          <tbody>
            <tr>
              <td>
                <h3>Your Email:</h3>
              </td>
              <td><span>{{ profile.email }}</span></td>
            </tr>

            <tr>
              <td>
                <h3>Phone: </h3>
              </td>
              <td><span>{{ profile.contact }}</span></td>
            </tr>

            <tr>
              <td>
                <h3>Address: </h3>
              </td>
              <td><span>{{ profile.address }}</span></td>
            </tr>

            <tr>
              <td>
                <h3>Pincode: </h3>
              </td>
              <td><span>{{ profile.pincode }}</span></td>
            </tr>

          </tbody>
        </table>
      </div>
    </div><br>

    <h2 style="font-size:30px; font-family:monospace;">Hello, {{ profile.name }}</h2>

    <div class="services">
      <h3 style="font-size:20px; font-family:monospace; margin-bottom:35px;">Looking for which service category?</h3>
      <div class="service-categories">
        <div class="service-categories">
          <div class="dropdown">
            <button>Cleaning</button>
            <div class="dropdown-content">
              <table v-if="cleaningServices.length > 0">
                <tr v-for="service in cleaningServices" :key="service.service_id">
                  <td>{{ service.service_name }}</td>
                  <td>{{ service.description }}</td>
                  <td>Rs. {{ service.price }}</td>
                  <td><button class="book" @click="bookService(service)" type="submit">Book</button></td>
                </tr>
              </table>
            </div>
          </div>
        </div>

        <div class="service-categories">
          <div class="dropdown">
            <button>Health & Wellness</button>
            <div class="dropdown-content">
              <table v-if="healthServices.length > 0">
                <tr v-for="service in healthServices" :key="service.service_id">
                  <td>{{ service.service_name }}</td>
                  <td>{{ service.description }}</td>
                  <td>Rs. {{ service.price }}</td>
                  <td><button class="book" @click="bookService(service)" type="submit">Book</button></td>
                </tr>
              </table>
            </div>
          </div>
        </div>

        <div class="service-categories">
          <div class="dropdown">
            <button>Saloon</button>
            <div class="dropdown-content">
              <table v-if="saloonServices.length > 0">
                <tr v-for="service in saloonServices" :key="service.service_id">
                  <td>{{ service.service_name }}</td>
                  <td>{{ service.description }}</td>
                  <td>Rs. {{ service.price }}</td>
                  <td><button class="book" @click="bookService(service)" type="submit">Book</button></td>
                </tr>
              </table>
            </div>
          </div>
        </div>

        <div class="service-categories">
          <div class="dropdown">
            <button>Home Decoration</button>
            <div class="dropdown-content">
              <table v-if="homedecorServices.length > 0">
                <tr v-for="service in hServices" :key="service.service_id">
                  <td>{{ service.service_name }}</td>
                  <td>{{ service.description }}</td>
                  <td>Rs. {{ service.price }}</td>
                  <td><button class="book" @click="bookService(service)" type="submit">Book</button></td>
                </tr>
              </table>
            </div>
          </div>
        </div>

        <div class="service-categories">
          <div class="dropdown">
            <button>Electrician</button>
            <div class="dropdown-content">
              <table v-if="electricianServices.length > 0">
                <tr v-for="service in electricianServices" :key="service.service_id">
                  <td>{{ service.service_name }}</td>
                  <td>{{ service.description }}</td>
                  <td>Rs. {{ service.price }}</td>
                  <td><button class="book" @click="bookService(service)">Book</button></td>
                </tr>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <p v-if="alert" class="alert">{{ alert }}</p>

    <div class="table">
      <p class="request-title">Requested Services: </p>
      <table v-if="serviceRequests.length > 0">
        <thead>
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
        </thead>
        <tbody>
          <tr v-for="record in serviceRequests" :key="record.request_id">
            <td>{{ record.request_id }}</td>
            <td>{{ record.service_name }}</td>
            <td>{{ record.pro_email }}</td>
            <td>{{ formatDate(record.request_date) }}</td>
            <td>{{ formatDate(record.schedule_date) }}</td>
            <td>{{ record.closed_date ? formatDate(record.closed_date) : 'Closing Date Pending' }}</td>
            <td>{{ record.status }}</td>
            <td>
              <button style="width:72px;" v-if="record.status === 'Requested'" @click="handleAction(record, 'close')">Close it?</button>
              <button style="width:97px; margin:0 14px; background-color: cornflowerblue;" v-if="record.status === 'Requested'" @click="handleAction(record, 'edit')">Edit Request</button>
              <button style="width:60px;" v-if="record.status === 'Requested' || record.status !== 'Closed by customer'" @click="cancelRequest(record)"
                class="delete-button">Cancel</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>Your service request is empty</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
axios.default.baseURL = 'http://loaclhost:5000';

export default {
  data() {
    return {
      profile: '',
      alert: '',
      services: [],
      serviceRequests: [],
      isProfileDropdownVisible: false,
    };
  },
  methods: {
    toggleProfileDropdown() {
      this.isProfileDropdownVisible = !this.isProfileDropdownVisible;
    },

    logoutuser() {
      localStorage.removeItem('authToken')
    },

    async handleAction(record, action){
      try{
        if(action == 'close'){
          const close = await axios.put(`/close_edit_request/close/${record.request_id}`,{},{
            headers:{
              Authorization:`${localStorage.getItem('authToken')}`
            }
          })

          if (close.status === 200) {
            const updatedRequest = this.serviceRequests.find(request => request.request_id === record.request_id);
            updatedRequest.status = 'Closed by customer';
          }
          
        }


        if(action == 'edit'){
          const edit = await axios.put(`/close_edit_request/edit/${record.request_id}`,{
            headers:{
              Authorization:`${localStorage.getItem('authToken')}`
            }
          })
          
        }
      }
      catch(error){
        console.log(error)
      }
    },

    async bookService(service) {
      try {
        const response = await axios.post('/request_service', { "service_id": service.service_id, "service_name": service.service_name },
          {
            headers: {
              Authorization: `${localStorage.getItem('authToken')}`
            }
          })
        if (response.status === 200) {
          this.serviceRequests.push(
            {
              request_id: response.data.request_id,
              service_name: service.service_name,
              pro_email: response.data.pro_email,
              status: response.data.status,
              closed_date: response.data.closed_date,
              request_date: response.data.request_date,
              schedule_date: response.data.schedule_date
            }
          )
        }
      }
      catch (error) {
        if (error.response.status === 404 || error.response.status === 400) {
          this.alert = error.response.data.message;
          setTimeout(() => {
            this.alert = ''
          }, 2000
          )
        }
      }
    },
    formatDate(date) {
      const option = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(date).toLocaleDateString('en', option);
    },
    async cancelRequest(record){
      try {
        const response = await axios.delete(`/cancel_request/${record.request_id}`,
          {
            headers: {
              Authorization: `${localStorage.getItem('authToken')}`
            }
          })
        if (response.status === 200) {
          this.serviceRequests = this.serviceRequests.filter(request => request.request_id !== record.request_id);
        }
      }
      catch (error) {
        if(error.response.status === 404){
          this.alert = error.response.message
          setTimeout(()=>{
            this.alert=''
          },3000)
        }
      }
    }
  },

  computed: {
    cleaningServices() {
      return this.services.filter(service => service.service_category === 'Cleaning');
    },
    healthServices() {
      return this.services.filter(service => service.service_category === 'Health and Wellness')
    },
    saloonServices() {
      return this.services.filter(service => service.service_category === 'Saloon')
    },
    electricianServices() {
      return this.services.filter(service => service.service_category === 'Electrician')
    },
    homedecorServices() {
      return this.services.filter(service => service.service_category === 'Home Decoration')
    },

  },
  async mounted() {
    try {
      const response = await axios.get('http://localhost:5000/customer_dashboard', {
        headers: {
          Authorization: `${localStorage.getItem('authToken')}`
        }
      });

      if (response.status === 200) {
        this.profile = response.data.profile;
        this.services = response.data.services;
        this.serviceRequests = response.data.service_req;
        console.log(this.serviceRequests)
      }
    }
    catch (error) {
      if (error.response.status === 401) {
        this.$router.push({ name: 'CustomerLogin', query: { 'message': "Please login to continue" } });
      }
    }
  }
};
</script>

<style scoped>
.customer-dashboard {
  font-family: 'Arial', sans-serif;
  padding: 20px;
}

.navbar {
  background-color: #333;
  color: white;
  padding: 10px;
  margin-top: -80px;
}

.navbar h1 {
  font-size: 210%;
}

.nav-links a {
  margin-left: 15px;
  text-decoration: none;
  color: #f0f0f0;
  font-size: 19px;
}

.profile-table tbody tr td {
  padding-top: 0px;
  padding-bottom: 0px;

}

.profile {
  position: relative;
  margin-top: 20px;
  z-index: 1;
}

.prof-button {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  width: 8%;
  float: right;
  z-index: 2;
}

.prof-button:hover {
  background-color: #45a049;
}

.dropdown-profile-content {
  position: absolute;
  top: 50px;
  right: 0;
  background-color: beige;
  width: 323px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  padding: 9px;
  z-index: 1000;
}

.services {
  margin-top: 30px;
  margin-bottom: 70px;
}

.dropdown-content button.book {
  width: 85px;
  height: 40px;
  font-size: 17px;
  padding: 12px;
  background-color: #1ed3cd;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
}

.service-categories {
  display: flex;
  gap: 56px;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}

.dropdown {
  position: relative;
}

.dropdown button {
  padding: 22px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  font-size: 18px;
  width: 191px;
}

.dropdown button:hover {
  background-color: #45a049;
}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  padding: 15px;
  width: 100%;
}

.dropdown:hover .dropdown-content {
  display: table;
}

.btn {
  padding: 10px 20px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 5px;
}

.btn:hover {
  background-color: #1976D2;
}

.request-title {
  font-size: 1.5em;
}

.table table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.table th,
.table td {
  padding: 7px;
  border: 1px solid #ddd;
  text-align: left;
}

.delete-button {
  background-color: #f44336;
  color: white;
}

.delete-button:hover {
  background-color: #e53935;
}

.alert {
  text-align: center;
  color: red;
  font-size: 1.2em;
  margin-top: 20px;
}

td {
  padding: 13px;
}
</style>
