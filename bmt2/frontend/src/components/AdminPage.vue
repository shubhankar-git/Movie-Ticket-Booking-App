<template>
  <div class="container mt-5">
    <Header />
    <h1 class="mb-4">Admin Page</h1>
    <div class="mb-3">
      <button class="btn btn-primary mr-2" @click="showManagement">Show Management</button>
      <button class="btn btn-success mr-2" @click="ExportCSV">Export Theatre Data</button>
      <button class="btn btn-warning" @click="PromoteToAdmin">Promote To Admin</button>
    </div>
    <div>
      <h2>Create Theatre</h2>
      <form @submit.prevent="createTheatre">
        <div class="form-group">
          <label for="name">Name:</label>
          <input type="text" id="name" class="form-control" v-model="theatreName" required>
        </div>
        <div class="form-group">
          <label for="place">Place:</label>
          <input type="text" id="place" class="form-control" v-model="theatrePlace" required>
        </div>
        <div class="form-group">
          <label for="capacity">Capacity:</label>
          <input type="number" id="capacity" class="form-control" v-model="theatreCapacity" required>
        </div>
        <button type="submit" class="btn btn-primary">Create Theatre</button>
        <button class="btn btn-secondary ml-2" @click="viewTheatres">View Available Theatres</button>
      </form>
      <div v-if="successMessage" class="alert alert-success mt-3" role="alert">
        {{ successMessage }}
      </div>
      <div v-if="errorMessage" class="alert alert-danger mt-3" role="alert">
        {{ errorMessage }}
      </div>
    </div>
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
      theatreName: '',
      theatrePlace: '',
      theatreCapacity: '',
      successMessage: '',
      errorMessage: '',
    };
  },
  methods: {
    createTheatre() {
      const newTheatreData = {
        name: this.theatreName,
        place: this.theatrePlace,
        capacity: this.theatreCapacity,
      };

      axios
        .post('http://127.0.0.1:5000/admin/theatres', newTheatreData, {
          headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
        })
        .then((response) => {
        
          this.successMessage = 'Theatre created successfully!';
          this.errorMessage = ''; // Clear any previous error message
          console.log('Server response:', response.data);
        })
        .catch((error) => {
          // Handle errors
          this.successMessage = ''; // Clear success message
          this.errorMessage = 'Error creating theatre: ' + error.message;
          console.error('Error creating theatre:', error.message);
        });
    },
   
    viewTheatres() {
      this.$router.push('/theatres');
    },
    ExportCSV() {
      this.$router.push('/ExportCSV');
    },
    showManagement() {
      this.$router.push('/showManagement');
    },
    PromoteToAdmin() {
      this.$router.push('/PromoteToAdmin');
    },
  },
};
</script>

<style>

</style>
