<template>
  <div>
    <div class="navbar">
      <h2>Welcome to Admin Panel</h2>
      <router-link :to="{ name: 'HomePage' }" @click="logoutUser">Logout</router-link>
      <router-link to="/admin_search">Search</router-link>
      <router-link :to="{ name: 'AdminSummary' }">Summary</router-link>
      <router-link to="/admin_dashboard">Home</router-link>
    </div>
    <h3>Professional Details:</h3>

    <div v-if="professional.length === 0">
      <p>No Professional Registered</p>
    </div>
    <div v-else>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Email ID</th>
            <th>Service Name</th>
            <th>Experience</th>
            <th>Address</th>
            <th>Approval Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="record in professional" :key="record.id">
            <td>{{ record.name }}</td>
            <td>{{ record.email }}</td>
            <td>{{ record.service_name }}</td>
            <td>{{ record.experience }} years</td>
            <td>{{ record.address }}</td>
            <td>{{ record.is_active ? 'Accept' : (record.status === 'Waiting for admin approval..' ? 'Waiting for response':'Reject') }}</td>
            <td>
              <button v-if="record.is_active" style="background-color: orangered"
                @click="accept_rejectPro(record)">Reject</button>
              <button v-else @click="accept_rejectPro(record)">Accept</button>
              <button style="background-color:cornflowerblue;"
                @click="$router.push({ name: 'ViewPro', query: { 'pro_id': record.id } })">View</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <h3>Services:</h3>
    <div v-if="services.length === 0">
      <p>No Services Exist</p>
    </div>
    <div v-else>
      <table>
        <thead>
          <tr>
            <th>Request Id</th>
            <th>Service Category</th>
            <th>Service Name</th>
            <th>Price</th>
            <th>Expected Time</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="record in services" :key="record.service_id">
            <td>{{ record.service_id }}</td>
            <td>{{ record.service_category }}</td>
            <td>{{ record.service_name }}</td>
            <td>Rs. {{ record.price }}</td>
            <td>{{ record.expected_time }}</td>
            <td>
              <button @click="Editservice(record)">Edit</button>
              <button style="background-color: orangered" @click="deleteService(record.service_id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p style="color:red;" v-if="message1">{{ message1 }}</p>
    </div>
    <button style="width: 7%" @click="addService">Add Service</button>
    <button style="width: 10%; background-color:dodgerblue;" @click="get_closed_service">Get closed services</button>

    <h3>Service Request:</h3>
    <div v-if="service_req.length === 0">
      <p>No Service Request Exist</p>
    </div>
    <div v-else>
      <table class="service-req">
        <thead>
          <tr>
            <th>Request Id</th>
            <th>Customer Email</th>
            <th>Assign Professional Email</th>
            <th>Services_name</th>
            <th>Request Date</th>
            <th>Closed Date</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="record in service_req" :key="record.service_id">
            <td>{{ record.request_id }}</td>
            <td>{{ record.customer_email }}</td>
            <td>{{ record.pro_email }}</td>
            <td>{{ record.service_name }}</td>
            <td>{{ record.request_date }}</td>
            <td>{{ record.close_date ? record.close_date : "Not closed yet" }} </td>
            <td>{{ record.status }}</td>

          </tr>
        </tbody>
      </table>
      <p style="color:red;" v-if="message1">{{ message1 }}</p>
    </div>

    <h3>Customer Details:</h3>
    <div v-if="customer.length === 0">
      <p>No Customer Registered</p>
    </div>
    <div v-else>
      <table>
        <thead>
          <tr>
            <th>Email</th>
            <th>Full Name</th>
            <th>Contact</th>
            <th>Address</th>
            <th>Gender</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="record in customer" :key="record.id">
            <td>{{ record.email }}</td>
            <td>{{ record.name }}</td>
            <td>{{ record.contact }}</td>
            <td>{{ record.address }}</td>
            <td>{{ record.gender }}</td>
            <td>{{ record.is_active ? 'Unblock' : 'Block' }}</td>
            <td>
              <button v-if="record.is_active" style="background-color: orangered;"
                @click="block_unblock(record)">Block</button>
              <button v-else @click="block_unblock(record)">Unblock</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="showEditForm" id="editForm" style="width:auto;">
      <h3>Edit Service</h3>
      <form class="edit-form" @submit.prevent="submitEdit">
        <label for="service_category">Service Category</label>
        <input type="text" v-model="editService.service_category" disabled />

        <label for="service_name">Service Name</label>
        <input type="text" v-model="editService.service_name" required />

        <label for="price">Price</label>
        <input type="number" v-model="editService.price" required />

        <label for="expected_time">Expected Time</label>
        <input type="text" v-model="editService.expected_time" required />

        <label for="description">Description</label>
        <textarea v-model="editService.description"></textarea>

        <button type="submit">Save Changes</button>
        <button type="button" @click="cancelEdit">Cancel</button>

        <p v-if="message">{{ message }}</p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AdminHome",

  data() {
    return {
      professional: [],
      customer: [],
      services: [],
      service_req: [],
      showEditForm: false,
      editService: {
        service_id: null,
        service_name: "",
        service_category: "",
        price: 0,
        expected_time: "",
        description: ""
      },
      message1: '',
      message: ''
    };
  },
  methods: {
    async get_closed_service() {
  try {
    // Step 1: Request the server to create the CSV file
    const response = await axios.get("http://localhost:5000/create_csv", {
      headers: {
        Authorization: `${localStorage.getItem("authToken")}`,
      },
    });

    if (response.status === 200) {
      const task_id = response.data.task_id; 

      let fileReady = false;
      let attempts = 0;
      while (!fileReady && attempts < 10) { 
        await new Promise((resolve) => setTimeout(resolve, 3000)); 

        // Check if the CSV file is ready
        const checkResponse = await axios.get(
          `http://localhost:5000/get_csv/${task_id}`,
          {
            headers: {
              Authorization: `${localStorage.getItem("authToken")}`,
            },
            responseType: "blob", // Ensure we receive the file properly
          }
        );

        if (checkResponse.status === 200) {
          fileReady = true; 

          const fileURL = window.URL.createObjectURL(new Blob([checkResponse.data]));
          const link = document.createElement("a");
          link.href = fileURL;
          link.setAttribute("download", "closed_services.csv"); 
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
        } else {
          attempts++;
        }
      }

      if (!fileReady) {
        alert("CSV file generation is taking too long. Please try again later.");
      }
    }
  } catch (error) {
    console.error("Error generating CSV:", error);
    alert("Failed to generate CSV. Please try again.");
  }
},

    
  async accept_rejectPro(record){
  try {
    const response = await axios.put(`http://localhost:5000/admin/accept_reject_pro/${record.id}`, {}, {
      headers: {
        Authorization: `${localStorage.getItem("authToken")}`,
      },
    });
    if (response.status === 200) {
      record.is_active = !record.is_active;
      console.log(response.data.message);
    }

  } catch (error) {
    console.log(error.response.data.message);
  }
},

Editservice(service) {

  this.editService.service_id = service.service_id;
  this.editService.expected_time = service.expected_time;
  this.editService.price = service.price;
  this.editService.service_category = service.service_category;
  this.editService.service_name = service.service_name;
  this.editService.description = service.description;
  this.showEditForm = true;

  this.$nextTick(() => {
    const scroll = document.getElementById("editForm")
    scroll.scrollIntoView({ behavior: "smooth" });
  })
},

cancelEdit() {
  this.showEditForm = false;
},

    async submitEdit() {
  try {
    const editData = await axios.put(
      `http://localhost:5000/admin/update_service/${this.editService.service_id}`,
      this.editService,
      {
        headers: {
          Authorization: `${localStorage.getItem("authToken")}`,
        },
      }
    );

    if (editData.status === 200) {
      this.message = editData.data.message;
    }
  } catch (error) {
    if (error.response.status === 401) {
      this.$router.push({
        name: "AdminLogin",
        query: { message: "You need to sign in first" },
      });
    }

    if (error.response.status === 400) {
      this.message = error.response.data.message;
    }
  }
},

logoutUser() {
  localStorage.removeItem("authToken");
},

    async deleteService(id) {
  try {
    const response = await axios.delete(`http://127.0.0.1:5000/admin/delete/${id}`, {
      headers: {
        Authorization: `${localStorage.getItem("authToken")}`,
      },
    });

    if (response.status === 200) {
      this.services = this.services.filter(service => service.service_id !== id);
      this.message1 = response.data.message;
      setTimeout(() => { this.message1 = '' }, 2000)
    }
  } catch (error) {
    if (error.response.status === 401) {
      this.$router.push({
        name: "AdminLogin",
        query: { message: "You need to sign in first" },
      });
    }

    if (error.response.status === 400) {
      this.message1 = error.response.data.message;

      setTimeout(() => { this.message1 = '' }, 2000)
    }
  }
},

addService() {
  this.$router.push({ name: "AddService" });
},

    async block_unblock(record) {
  try {

    const response = await axios.put(
      `http://localhost:5000/admin/block_unblock_user/${record.id}`,
      {},
      {
        headers: {
          Authorization: `${localStorage.getItem("authToken")}`,
        },
      }
    );

    if (response.status === 200) {
      record.is_active = !record.is_active;
      console.log(response.data.message);
    }
  } catch (error) {
    console.log(error.message);
  }
}
  },

  async mounted() {
  try {
    const response = await axios.get("http://127.0.0.1:5000/admin_home", {
      headers: {
        Authorization: `${localStorage.getItem("authToken")}`,
      },
    });

    if (response.status === 200) {
      this.professional = response.data.professional;
      this.customer = response.data.customer;
      this.services = response.data.services;
      this.service_req = response.data.service_req;
    }
  } catch (error) {
    if (error.response.status === 401) {
      this.$router.push({
        name: "AdminLogin",
        query: { message: "You need to sign in first" },
      });
    }
  }
}
};
</script>

<style scoped>
.navbar {
  margin-top: -60px;
  background-color: green;
  color: white;
}

h3 {
  margin-top: 53px;
  margin-left: 1%;
  font-size: 24px;
  text-align: center;
}

.service-req tbody tr td {
  padding: 15px;
}

.service-req thead tr th {
  padding: 35px;
  padding-bottom: 10px;
  padding-top: 0px;
}

td {
  padding: 0px 45px;
}

.navbar a {
  font-size: 19px;
  float: right;
  display: block;
  text-align: center;
  padding: 0px 16px;
  text-decoration: none;
  color: azure;
  margin-top: -13px;
  margin-bottom: 28px;
}

h2 {
  font-size: xx-large;
  font-weight: bolder;
  margin-bottom: -35px;
  padding: 20px;
  margin-top: 2px;
  font-family: Cambria, Cochin, Georgia, Times, "Times New Roman", serif;
}

p {
  text-align: center;
  font-size: 17px;
}

table {
  margin: auto;
}

button {
  width: 70px;
  margin: 3px 7px 12px 0px;
}

.edit-form {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.edit-form input,
.edit-form textarea {
  margin: 5px 0;
  padding: 10px;
  width: 100%;
  max-width: 300px;
}

.edit-form button {
  width: 108px;
  margin-top: 0px;
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px;
  cursor: pointer;
  border-radius: 5px;
}

button:hover {
  background-color: #45a049;
}

button[type="button"] {
  background-color: #f44336;
}

button[type="button"]:hover {
  background-color: #e41f19;
}

div[style="width:18%"] {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100%;
}

h3 {
  margin-bottom: 20px;
}

p {
  color: green;
  text-align: center;
}
</style>
