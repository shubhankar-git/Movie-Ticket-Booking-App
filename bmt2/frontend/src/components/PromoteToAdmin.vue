<template>
    <div>
      <Header />
      <h1>Promote User to Admin</h1>
      <form @submit.prevent="promoteUser">
        <div>
          <label for="username">Username or User ID:</label>
          <input type="text" id="username" v-model="usernameOrUserId" required>
        </div>
        <div>
          <button type="submit">Promote to Admin</button>
        </div>
      </form>
      <p v-if="message" :class="{ 'success-message': success, 'error-message': !success }">{{ message }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import Header from './HeaderAdmin.vue';
  export default {
    components: {
    Header,
  },
    data() {
      return {
        usernameOrUserId: '',
        message: '',
        success: null,
      };
    },
    
    methods: {
      promoteUser() {
        const accessToken = localStorage.getItem('access_token');

// Prepare the headers with the authorization token
const headers = {
  Authorization: `Bearer ${accessToken}`,
};
        axios
          .post('http://127.0.0.1:5000/promote', 
          { usernameOrUserId: this.usernameOrUserId }, { headers })
          .then(response => {
            this.message = response.data.message;
            this.success = true;
          })
          .catch(error => {
            this.message = 'Error promoting user to admin.';
            this.success = false;
            console.error(error);
          });
      },
    },
  };
  </script>
  
  <style>
  .success-message {
    color: green;
  }
  
  .error-message {
    color: red;
  }
  </style>
  