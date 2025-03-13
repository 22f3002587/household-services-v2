<template>
  <div class="customer-dashboard">
    <div class="navbar">
      <h1>Welcome to Customer Dashboard</h1>
      <div class="nav-links">
        <a href="/logout_user">Logout</a>
        <a href="/customer_search">Search</a>
        <a href="#">Home</a>
      </div>
    </div>

    <div class="profile">
      <button class="prof-button" @click="toggleProfileDropdown">View Profile</button><br><br>
      <div v-if="isProfileDropdownVisible" class="dropdown-profile-content">
        <img src="/static/image.png" alt="user-image">
        <h3>Hello</h3>
        <h3>Your Email: <span>{{ user_data.email }}</span></h3>
        <h3>Experience: </h3>
        <h3>Specialisation:</h3>
        <h3>Admin Approval:</h3>
      </div>
    </div><br>

    <h2 style="font-size:30px; font-family:monospace;">Hello, {{ user_data.fullname }}</h2>

    <div class="services">
      <h3 style="font-size:20px; font-family:monospace;">Looking for which service category?</h3>
      <div v-for="category in serviceCategories" :key="category.name" class="dropdown ">
        <button>{{ category.name }}</button>
        <div class="dropdown-content">
          <table v-if="category.services.length > 0">
            <tr v-for="service in category.services" :key="service.service_id">
              <td>{{ service.service_name }}</td>
              <td>{{ service.description }}</td>
              <td>Rs. {{ service.base_price }}</td>
              <td>
                <div>
                  <input type="hidden" name="form_id" :value="category.name.toLowerCase()">
                  <input type="hidden" name="service_id" :value="service.service_id">
                  <input type="hidden" name="customer_email" :value="user_data.email">
                  <button class="btn" type="submit">Book</button>
                </div>
              </td>
            </tr>
          </table>
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
            <td>{{ record.professional_id }}</td>
            <td>{{ formatDate(record.requested_date) }}</td>
            <td>{{ formatDate(record.scheduled_date) }}</td>
            <td>{{ record.closed_date ? formatDate(record.closed_date) : 'Closing Date Pending' }}</td>
            <td>{{ record.status }}</td>
            <td>
              <button v-if="record.status === 'Requested'" @click="handleAction(record, 'close')">Close it?</button>
              <button v-if="record.status === 'Requested'" @click="handleAction(record, 'edit')">Edit Request</button>
              <button v-if="record.status !== 'Professional Dismissed'" @click="handleAction(record, 'delete')" class="delete-button">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>Your service request is empty</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      user_data: {
        fullname: 'John Doe',
        email: 'johndoe@example.com',
      },
      alert: '',
      serviceCategories: [
        {
          name: 'Cleaning',
          services: [
            { service_id: 1, service_name: 'House Cleaning', description: 'Thorough cleaning of your house', base_price: 500 },
            { service_id: 2, service_name: 'Office Cleaning', description: 'Office space cleaning', base_price: 1000 },
          ],
        },
        {
          name: 'Home Decoration',
          services: [
            { service_id: 3, service_name: 'Living Room Decor', description: 'Decorate your living room', base_price: 1500 },
          ],
        },
        // Other categories...
      ],
      serviceRequests: [
        { request_id: 1, service_name: 'House Cleaning', professional_id: 'P123', requested_date: new Date(), scheduled_date: new Date(), closed_date: null, status: 'Requested' },
        { request_id: 2, service_name: 'Office Cleaning', professional_id: 'P124', requested_date: new Date(), scheduled_date: new Date(), closed_date: null, status: 'Requested' },
      ],
      isProfileDropdownVisible: false,
    };
  },
  methods: {
    formatDate(date) {
      return new Date(date).toLocaleDateString();
    },
    toggleProfileDropdown() {
      this.isProfileDropdownVisible = !this.isProfileDropdownVisible;
    },
    handleAction(record, action) {
      console.log(`${action} action triggered for request ${record.request_id}`);
    },
  },
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
  position: relative;
  margin-top:-80px;
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

.profile {
  position: relative;
  margin-top: 20px;
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
}

.prof-button:hover {
  background-color: #45a049;
}

.dropdown-profile-content {
  position: absolute;
  top: 50px;
  right: 0;
  background-color: #f9f9f9;
  width: 250px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  padding: 20px;
}

.services {
  margin-top: 30px;
}

.dropdown {
  margin: 10px 0;
}

.dropdown button {
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
}

.dropdown button:hover {
  background-color: #45a049;
}

.dropdown-content {
  display: none;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  padding: 15px;
}

.dropdown:hover .dropdown-content {
  display: block;
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

.table th, .table td {
  padding: 10px;
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
</style>
