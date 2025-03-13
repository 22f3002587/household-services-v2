<template>
    <div class="admin-dashboard">
        <div class="dashboard-header">
            <h1>Welcome To Summary Panel</h1>
        </div>

        <div class="dashboard-summary">
            <div class="summary-section">
                <h3>Professional Summary</h3>
                <div class="summary-item">
                    <p>Total Professionals: <strong>{{ pro.totalPro }}</strong></p>
                    <p>Pending Approvals: <strong>{{ pro.pendingApprovals }}</strong></p>
                    <p>Rejected Professionals: <strong>{{ pro.blockedPro }}</strong></p>
                </div>
            </div>

            <div class="summary-section">
                <h3>Service Request Summary</h3>
                <div class="summary-item">
                    <p>Total Service Requests: <strong>{{ service_req.total_req}}</strong></p>
                    <p>Pending Requests: <strong>{{ service_req.pending_req }}</strong></p>
                    <p>Completed Requests: <strong>{{ service_req.completed_req }}</strong></p>
                    <p>Dismissed by Professional: <strong>{{ service_req.pro_dissmissed }}</strong></p>
                </div>
            </div>

            <div class="summary-section">
                <h3>Services Summary</h3>
                <div class="summary-item">
                    <p>Total Services:<strong>{{ services.totalService }}</strong></p>
                    <p>Vacant Services: <strong>{{ services.vacantService }}</strong></p>
                    <p>Registered Services: <strong>{{ services.registerService }}</strong></p>
                </div>
                <button @click="createNewService" class="btn btn-primary">Create New Service</button>
            </div>

            <div class="summary-section">
                <h3>Customer Summary</h3>
                <div class="summary-item">
                    <p>Total Customers: <strong>{{ customer.totalCustomer }}</strong></p>
                    <p>Blocked Customers: <strong>{{ customer.blockedCustomer }}</strong></p>
                    <p>Active Customers: <strong>{{ customer.activeCustomer }}</strong></p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            pro:{
                totalPro:'',
                pendingApprovals:'',
                blockedPro:''
            },
            services:{
                totalService:'',
                vacantService:'',
                registerService:'',
            },
            customer:{
                totalCustomer:'',
                blockedCustomer:'',
                activeCustomer:''
            },
            service_req:{
                total_req:'',
                pending_req:'',
                completed_req:'',
                pro_dissmissed:''

            }
        };
    },
    methods: {
        createNewService() {
           this.$router.push({name:'AddService'});
        },
        sendDailyReminder() {
            // Logic to send daily reminder
            console.log("Daily reminder sent to service professionals.");
        },
        viewAllActivities() {
            // Logic to view all activities
            console.log("Viewing all activities...");
        }
    },
    async mounted() {
        try {
            const response = await axios.get("http://localhost:5000/admin_summary", {
                headers: {
                    Authorization: `${localStorage.getItem('authToken')}`
                }
            });
            if(response.status === 200){
                this.pro.totalPro = response.data.totalPro;
                this.pro.pendingApprovals = response.data.pendingApproval;
                this.pro.blockedPro = response.data.blockedPro;
                this.services.totalService = response.data.totalServices;
                this.services.vacantService = response.data.vacantServices;
                this.services.registerService = response.data.registerServices;
                this.customer.totalCustomer = response.data.totalCustomer;
                this.customer.blockedCustomer = response.data.blockedCustomer;
                this.customer.activeCustomer = response.data.activeCustomer;
                this.service_req.total_req = response.data.totalreq;
                this.service_req.pending_req = response.data.pending_req;
                this.service_req.completed_req = response.data.complete_req;
                this.service_req.pro_dissmissed = response.data.pro_dismissed;
                
            }
        }
        catch (error) {
            if (error.response.status === 401) {
                this.$router.push({ name: 'AdminLogin', query: { message: 'You need to sign in first' } });
            }
        }
    }
};
</script>

<style scoped>
.admin-dashboard {
    font-family: Arial, sans-serif;
    padding: 20px;
}

.dashboard-header h1 {
    color: #333;
}

.dashboard-summary {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-top: 30px;
}

.summary-section {
    background-color: #f4f4f4;
    padding: 15px;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.summary-item p {
    margin: 8px 0;
    font-size: 14px;
}

h3 {
    font-size: 18px;
    color: #007bff;
}

button {
    padding: 10px;
    font-size: 14px;
    border-radius: 5px;
    border: none;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

button:hover {
    opacity: 0.8;
}

.btn-primary {
    background-color: #007bff;
    color: white;
    width:23%;
}

.btn-primary:hover {
    background-color: #0056b3;
}

.btn-warning {
    background-color: #f39c12;
    color: white;
}

.btn-warning:hover {
    background-color: #e67e22;
}

.btn-info {
    background-color: #17a2b8;
    color: white;
}

.btn-info:hover {
    background-color: #138496;
}

.activity-feed ul {
    list-style-type: none;
    padding: 0;
}

.activity-feed li {
    background-color: #f9f9f9;
    padding: 10px;
    border-radius: 5px;
    margin: 5px 0;
}

.activity-feed button {
    margin-top: 10px;
}
</style>