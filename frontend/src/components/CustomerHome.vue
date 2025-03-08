<template>
  <p>Customer Dashboard</p>
  {{this.name}}
</template>


<script>
import axios from 'axios'
export default{
  data(){
    return{
      name:'',
      email:''
    }
  },
  methods:{
    async fetchData(){
      console.log(localStorage.getItem('authToken'))
      try{
        const response = await axios.get('http://localhost:5000/customer_dashboard', {headers:{
          Authorization: `Bearer ${localStorage.getItem('authToken')}`
        }})


        if(response.status === 200){
          this.name = response.data.name
          this.email = response.data.email
        }
      }
      catch(error){
        if(error.response){
          console.log(error.response)
          alert('Something went wrong')
        }
      }
    }
  },
  mounted(){
    this.fetchData()
  }
}


</script>


<style>

</style>