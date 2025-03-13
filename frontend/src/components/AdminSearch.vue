<template>
    <div>
        <div class="navbar">
            <h2>Welcome to Admin Panel</h2>
            <router-link to="/" @click="logout">Logout</router-link>
            <a href="/admin_search">Search</a>
            <router-link :to="{ name: 'AdminHome' }">Home</router-link>
        </div>

        <div class="content">
            <h3>Search a professional</h3>
            <form @click.prevent="searchProfessional">
                <input type="hidden" name="form_id" value="id1" />
                <label for="id1">Search By: </label>
                <select v-model="searchBy" id="id1" required>
                    <option value="">Select</option>
                    <option value="email">Email</option>
                    <option value="name">Name</option>
                    <option value="service_name">Service</option>
                </select>
                <input type="text" v-model="searchData" required />
            </form>
            <div>
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Email ID</th>
                            <th>Service Name</th>
                            <th>Experience</th>
                            <th>Action</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="record in filteredPro" :key="record.email">
                            <td>{{ record.name }}</td>
                            <td>{{ record.email }}</td>
                            <td>{{ record.service_name }}</td>
                            <td>{{ record.experience }}</td>
                            <td>
                                <button v-if="record.is_active" style="background-color: orangered"
                                    @click="accept_rejectPro(record)">Reject</button>
                                <button v-else @click="accept_rejectPro(record)">Accept</button>
                            </td>
                            <td>{{ record.is_active ? 'Accept' : (record.status === 'Waiting for admin approval..' ?
                                'Waiting for response':'Reject') }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";
export default {
    data() {
        return {
            pro: '',
            searchBy: "",
            searchData: ""
        }
    },

    computed: {
        filteredPro() {
            if (this.searchData === '') {
                return this.pro
            }

            if (this.searchBy === 'email') {
                return this.pro.filter((pro) => {
                    return pro.email.toLowerCase().includes(this.searchData.toLowerCase())
                })
            }
            if (this.searchBy === 'name') {
                return this.pro.filter((pro) => {
                    return pro.name.toLowerCase().includes(this.searchData.toLowerCase())
                })
            }
            if (this.searchBy === 'service_name') {
                return this.pro.filter((pro) => {
                    return pro.service_name.toLowerCase().includes(this.searchData.toLowerCase())
                })
            }
            console.log(this.searchBy)
            return this.pro
        }
    },
    methods: {
        logout() {
            localStorage.removeItem("authToken");
        },

        async accept_rejectPro(record) {
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

    },
    async mounted() {
        try {
            const response = await axios.get("http://localhost:5000/admin_home", {
                headers: {
                    Authorization: `${localStorage.getItem("authToken")}`
                }
            });
            if (response.status === 200) {
                this.pro = response.data.professional;
                console.log(this.pro);

            }
        } catch (error) {
            if (error.response.status === 401) {
                this.$router.push({
                    name: 'AdminLogin',
                    query: { message: 'You need to sign in first' }
                });
            }
        }

    }
}
</script>

<style scoped>
.navbar {
    background-color: green;
    color: white;
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
    margin-top: -60px;
    font-family: Cambria, Cochin, Georgia, Times, "Times New Roman", serif;
}

.content {
    padding: 20px;
    font-family: Arial, sans-serif;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    margin: 60px;
}

h3 {
    margin-bottom: 20px;
    color: #333;
}

label {
    margin-right: 10px;
    font-weight: bold;
}

input[type="text"],
select {
    padding: 10px;
    margin: 10px 0;
    border: 1px solid #ccc;
    border-radius: 4px;
    width: calc(100% - 22px);
    /* Full width minus padding */
    max-width: 150px;
    /* Limit max width */
}

button {
    background-color: green;
    border: none;
    color: white;
    padding: 10px 15px;
    cursor: pointer;
    border-radius: 4px;
    transition: background-color 0.3s;
    margin-left: 5px;
    width: 58%;
}

button:hover {
    background-color: darkgreen;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

th,
td {
    border: 1px solid #ddd;
    padding: 12px;
    text-align: left;
}

th {
    background-color: #4caf50;
    color: white;
}

tr:nth-child(even) {
    background-color: #f2f2f2;
}
</style>