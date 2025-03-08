<template>
  <div>
    <div class="navbar">
      <h2>Welcome to Admin Panel</h2>
      <a href="/logout_user">Logout</a>
      <a href="/admin_search">Search</a>
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
            <th>Approval Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="record in professional" :key="record.id">
            <td>{{ record.name }}</td>
            <td>{{ record.email }}</td>
            <td>{{ record.service_name }}</td>
            <td>{{ record.experience }}</td>
            <td>{{ record.status }}</td>
            <td>
              <button @click="acceptPro(record.id)">Accept</button>
              <button
                style="background-color: orangered"
                @click="rejectPro(record.id)"
              >
                Reject
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <h3>Services:</h3>
    <div v-if="services.length === 0"><p>No Services Exist</p></div>
    <div v-else>
      <table>
        <thead>
          <tr>
            <th>Service Id</th>
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
            <td>{{ record.price }}</td>
            <td>{{ record.expected_time }}</td>
            <td>
              <button @click="Editservice(record)">Edit</button>
              <button
                style="background-color: orangered"
                @click="deleteService(record.id)"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <button style="width: 7%" @click="addService">Add Service</button>

    <h3>Customer Details:</h3>
    <div v-if="services.length === 0"><p>No Customer Registered</p></div>
    <div v-else>
      <table>
        <thead>
          <tr>
            <th>Email</th>
            <th>Full Name</th>
            <th>Contact</th>
            <th>Address</th>
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
            <td>{{ record.status }}</td>
            <td>
              <button @click="block(record.id)">Block</button>
              <button style="background-color: orangered" @click="unblock(record.id)">Unblock</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="showEditForm" class="edit-form">
      <h3>Edit Service</h3>
      <form @submit.prevent="submitEdit">
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

        <p v-if="message">{{message}}</p>
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
      showEditForm: false,
      editService: {
        service_id: null,
        service_name: "",
        service_category: "",
        price: 0,
        expected_time: "",
        description:""
      },
      message:''
    };
  },
  methods: {
    acceptPro(id) {
      console.log(id);
    },

    rejectPro(id) {
      console.log(id);
    },

    Editservice(service) {
      // console.log(service.expected_time, service.service_category, service.service_id)
      
      this.editService.service_id = service.service_id;
      this.editService.expected_time = service.expected_time;
      this.editService.price = service.price;
      this.editService.service_category = service.service_category
      this.editService.service_name = service.service_name;
      this.editService.description = service.description
      console.log(this.editService)
      this.showEditForm = true;
    },

    cancelEdit() {
      this.showEditForm = false;
    },

    async submitEdit() {
      try {
        console.log(this.editService)
        const editData = await axios.put(
          `http://localhost:5000/admin/update_service/${this.editService.service_id}`,
          this.editService,
          {
            headers: {
              Authorization: `${localStorage.getItem("authToken")}`,
            },
          }
        );

        if(editData.status === 200){
          this.message = editData.data.message

        }
      } catch (error) {
        console.log("here is error")
        console.log(error.message)
      }
    },

    deleteService(id) {
      console.log(id);
    },
    async addService() {
      this.$router.push({ name: "AddService" });
    },
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
      }
    } catch (error) {
      if (error.response.status === 401) {
        this.$router.push({
          name: "AdminLogin",
          query: { message: "You need to sign in first" },
        });
      }
    }
  },
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
</style>
