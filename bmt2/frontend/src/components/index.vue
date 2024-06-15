<template>
  <div id="app" class="container">
    <h1 class="mt-5">Welcome to the Ticket Booking App</h1>
    <p class="lead">This is the homepage of the ticket booking app.</p>
    <p class="lead">You can login or register to start booking tickets.</p>
    
    <router-link v-if="!isLoggedIn" :to="{ path: '/login' }" class="btn btn-primary">Login</router-link>
    <router-link v-else-if="isAdmin" :to="{ path: '/AdminPage' }" class="btn btn-success">Admin Dashboard</router-link>
    <router-link v-else :to="{ path: '/UserDashboard' }" class="btn btn-info">User Dashboard</router-link>
    
    <div class="mt-3">
      <a href="/register" class="btn btn-secondary">Register</a>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  computed: {
    isLoggedIn() {
      // Check if the access_token is present in localStorage
      return localStorage.getItem('access_token') !== null;
    },
    isAdmin() {
      // Check if the user has the admin role 
      const userRoles = localStorage.getItem('roles');
      return userRoles && userRoles.includes('admin');
    },
  },
};
</script>

