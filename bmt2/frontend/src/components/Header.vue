<template>
    <div class="header">
      <div v-if="userName">Welcome, {{ userName }}</div>

      <button @click="Home">Home</button>
     
      <button @click="viewBookedTickets">Booked Tickets</button>

      <button @click="logout">Logout</button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
        return {
            userName: null
        };},
    mounted() {
        // Retrieve user name from local storage
        this.userName = localStorage.getItem('username');
    },
    methods: {
      logout() {
      // Clear user authentication state 
      localStorage.removeItem('access_token');
  
      this.$router.push('/');
    },
  
     
  
      viewBookedTickets() {
        try {
           
            this.$router.push('/booked')
        } catch (error) {
          console.error(error);
        }
      },
      Home() {
        try {
           
            this.$router.push('/UserDashboard')
        } catch (error) {
          console.error(error);
        }
      },
    },
  };
  </script>
  
  <style>
  
  .header {
   
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #f2f2f2;
    padding: 10px;
  }
  .header button {
    margin-right: 10px;
    padding: 5px 10px;
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  </style>
  