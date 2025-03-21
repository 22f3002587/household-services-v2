<template>
    <div class="container">
        <h1>Professional Details</h1>
        <table>
            <tr>
                <td class="field">Full Name:</td>
                <td>{{ pro.fullname }}</td>
            </tr>
            <tr>
                <td class="field">Email:</td>
                <td>{{ pro.email }}</td>
            </tr>
            <tr>
                <td class="field">Service Provided:</td>
                <td>{{ pro.service_name }}</td>
            </tr>
            <tr>
                <td class="field">Experience:</td>
                <td>{{ pro.experience }} Years</td>
            </tr>
            <tr>
                <td class="field">User Rating:</td>
                <td>{{ pro.avg_rating }} out of 5</td>
            </tr>
            <tr>
                <td class="field">Address:</td>
                <td>{{ pro.address }}</td>
            </tr>
            <tr>
                <td class="field">Pincode:</td>
                <td>{{ pro.pincode }}</td>
            </tr>
        </table>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            pro:''
        };
    },

    async mounted() {
        let pro_id = this.$route.query.pro_id
        try {
            const response = await axios.get(`admin/view_pro/${pro_id}`, {
                headers:{
                    Authorization:`${localStorage.getItem('authToken')}`
                }
            })
            if(response.status === 200){
                this.pro = response.data
            }
        }
        catch (error) {
            if (error.response.status === 401) {
                this.$router.push({ name: 'AdminLogin', query: { message: 'You need to signin first'} })
            }
        }
    }
}
</script>

<style scoped>
.container {
    background-color: #fff;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    padding: 20px;
    max-width: 600px;
    width: 100%;
    margin: auto;
}

h1 {
    text-align: center;
    color: black;
    font-size: 24px;
    margin-bottom: 20px;
}

table {
    width: 100%;
    border-collapse: collapse;
}

.field {
    font-size: 1rem;
    font-weight: bold;
    color: #343a40;
    padding: 10px;
    background-color: #e9ecef;
}

td {
    padding: 10px;
    border-bottom: 1px solid #dee2e6;
}

button {
    background-color: #007bff;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    display: block;
    margin: 20px auto;
    text-align: center;
}

button:hover {
    background-color: #0056b3;
}
</style>