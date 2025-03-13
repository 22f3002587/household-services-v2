<template>
    <div class="dashboard-container">
        <div class="navbar">
            <h2>Welcome to Professional Dashboard</h2>
            <div style="margin-left:22%" class="navbar-links">
                <router-link :to="{name:'ProHome'}">Home</router-link>
                <router-link :to="{name:'HomePage'}" @click="logoutUser">Logout</router-link>
            </div>
        </div>


        <div class="content-wrapper">
            <div class="main-content">
                <div class="service-requests">
                    <h3 class="heading">Today's Service Request</h3>
                    <div v-if="customer_details.length === 0">
                        <p class="message">No service request received yet</p>
                    </div>
                    <div v-else>
                        <table class="service-table">
                            <thead>
                                <tr>
                                    <th>Customer Email</th>
                                    <th>Customer Name</th>
                                    <th>Contact No.</th>
                                    <th>Address</th>
                                    <th>Scheduled Date</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(record, index) in customer_details" :key="index">
                                    <td>{{ record.customer_email }}</td>
                                    <td>{{ record.customer_name }}</td>
                                    <td>{{ record.contact }}</td>
                                    <td>{{ record.address }}</td>
                                    <td>{{ record.schedule_date }}</td>
                                    <td>
                                        <button>Accept</button> 
                                        <button>Dismiss</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>


                <p v-if="alert" class="alert-message">{{ alert }}</p>

                <div class="closed-services">
                    <h3 class="heading">Closed Services</h3>
                    <div v-if="closed_services.length">
                        <table class="service-table">
                            <thead>
                                <tr>
                                    <th>Request ID</th>
                                    <th>Service ID</th>
                                    <th>Customer ID</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(record, index) in closed_services" :key="index">
                                    <td>{{ record.request_id }}</td>
                                    <td>{{ record.service_id }}</td>
                                    <td>{{ record.customer_id }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <p v-else class="message">No service closed yet</p>
                </div>
            </div>


            <div class="sidebar">
                <div>
                    <img src="https://media.istockphoto.com/id/1300845620/vector/user-icon-flat-isolated-on-white-background-user-symbol-vector-illustration.jpg?s=612x612&w=0&k=20&c=yBeyba0hUkh14_jgv1OKqIH0CCSWU_4ckRkAoy2p73o=" alt="user-image">
                    <h3>Welcome {{ prof_data.name }}</h3>
                    <table>
                        <tbody>
                            <tr>
                                <td>
                                    <h4>Your Email:</h4>
                                </td>
                                <td><span>{{ prof_data.email }}</span></td>
                            </tr>
                            <tr>
                                <td>
                                    <h4>Experience:</h4>
                                </td>
                                <td><span>{{ prof_data.experience }} Years</span></td>
                            </tr>
                            <tr>
                                <td>
                                    <h4>Address:</h4>
                                </td>
                                <td><span>{{ prof_data.address }}</span></td>

                            </tr>
                            <tr>
                                <td>
                                    <h4>Specialisation:</h4>
                                </td>
                                <td><span>{{ prof_data.service_name }}</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>

            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";
// import { format } from 'date-fns'
export default {
    data() {
        return {
            customer_details: [],
            closed_services:[],
            alert: '',
            prof_data: ''
        }
    },
    methods: {
        logoutUser() {
            localStorage.removeItem('authToken')
        }
    },
    async mounted() {
        try {
            const response = await axios.get('http://localhost:5000/professional_dashboard', {
                headers: {
                    Authorization: `${localStorage.getItem('authToken')}`
                }
            });

            if (response.status === 200) {
                this.prof_data = response.data.pro_detail
                this.customer_details = response.data.service_req
                this.closed_services = response.data.closed_req

            }
        } catch (error) {
            if (error.response.status === 401) {
                this.$router.push({ name: 'ProLogin', query: { message: 'You need to sign in first' } });
            }
        }

    }
}
</script>

<style scoped>
.dashboard-container {
    font-family: Arial, sans-serif;
    padding: 20px;
}

.navbar {
    background-color: #2c3e50;
    color: white;
    padding: 31px;
    display: flex;
    align-items: flex-end;
    width: 96%;
    margin-top: -80px;
    justify-content:flex-end;
}

.navbar h2 {
    font-size: 24px;
    margin: 0;
    margin-left: 232px;
}

.navbar-links a {
    color: #ecf0f1;
    text-decoration: none;
    margin: 0px 31px;
    font-size: 18px;
    float: left;
}

.navbar-links a:hover {
    color: #3498db;
}

.content-wrapper {
    display: flex;
    /* Flexbox for the two main sections below navbar */
    gap: 20px;
    margin-top: 20px;
}

.main-content {
    flex: 0 0 80%;
    /* Main content takes up 80% of the screen */
}

.sidebar {
    flex: 0 0 15%;
    /* Sidebar (professional details) takes up 30% of the screen */
    background-color: #ecf0f1;
    padding: 20px;
    border-radius: 8px;
    height: 55vh;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    margin-top: 51px;
}

.profile-container {
    margin-top: 30px;
    text-align: center;
    margin-bottom: 20px;
}

.view-profile-btn {
    background-color: #3498db;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    width: 9%;
    float: inline-end;
}

.view-profile-btn:hover {
    background-color: #2980b9;
}

span {
    margin-left: 10px;
}

.profile-container:hover .dropdown-content {
    display: block;
}

.profile-img {
    width: 90px;
    border-radius: 50%;
    margin-bottom: 10px;
}

.profile-info {
    font-size: 20px;
    font-weight: bold;
    margin: 10px 0;
}

.profile-container p {
    font-size: 16px;
    margin: 10px 0;
}

.profile-container span {
    color: #555;
    margin-left: 5px;
}

.edit-profile-btn {
    background-color: black;
    color: white;
    padding: 8px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 14px;
}

.edit-profile-btn:hover {
    background-color: #444;
}

.service-requests,
.closed-services {
    margin-top: 40px;
}

.heading {
    font-size: 22px;
    margin-bottom: 15px;
    color: #2c3e50;
}

.service-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
    border-radius: 10px;
    overflow: hidden;
}

.service-table th,
.service-table td {
    padding: 12px;
    text-align: center;
    border: 1px solid #ddd;
}

img{
    width: 43%;
    border-radius: 50%;
}

.service-table th {
    background-color: #34495e;
    color: white;
}

.service-table td {
    background-color: #f9f9f9;
}

.service-table tr:hover {
    background-color: #f1f1f1;
}

.action-btn {
    background-color: #27ae60;
    color: white;
    padding: 8px 16px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 14px;
    margin-right: 10px;
}

.action-btn:hover {
    background-color: #2ecc71;
}

.alert-message {
    text-align: center;
    color: red;
    font-weight: bold;
    font-size: 18px;
}

.message {
    text-align: center;
    color: #7f8c8d;
    font-size: 16px;
    font-weight: bold;
}

button{
    width: 38%;
    padding: 10px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin: 5px;
}
</style>
