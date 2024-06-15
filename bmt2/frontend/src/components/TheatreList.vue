<template>
  <div class="container">
    <Header />
    <h2 class="mt-4">Available Theatres</h2>
    <!-- Success alert message for saving edit -->
    <div v-if="successMessage" class="alert alert-success mt-3" role="alert">
      {{ successMessage }}
    </div>
    <!-- Error alert message for saving edit -->
    <div v-if="errorMessage" class="alert alert-danger mt-3" role="alert">
      {{ errorMessage }}
    </div>
    <ul v-if="theatres.length > 0" class="list-group mt-4">
      <li v-for="theatre in theatres" :key="theatre.id" class="list-group-item">
        <h3 v-if="!theatre.editing">{{ theatre.name }}</h3>
        <input v-if="theatre.editing" v-model="theatre.name" class="form-control" />
        <p class="mb-2">Location: {{ theatre.place }}</p>
        <p class="mb-2">Capacity: {{ theatre.capacity }}</p>
        <button @click="addShow(theatre)" class="btn btn-primary mr-2">Add Show</button>
        <button v-if="!theatre.editing" @click="toggleEdit(theatre)" class="btn btn-secondary mr-2">Edit</button>
        <button v-else @click="saveEdit(theatre)" class="btn btn-success mr-2">Save</button>
        <button v-if="!theatre.editing" @click="deleteTheatre(theatre.id)" class="btn btn-danger">Delete</button>
      </li>
    </ul>
    <p v-else class="mt-4">No theaters found.</p>
  </div>
</template>
<script>
import Header from './HeaderAdmin.vue';

export default {
  components: {
    Header,
  },
  data() {
    return {
      theatres: [],
      loading: true,
      successMessage: '', // Success message for saving edit
      errorMessage: '',   // Error message for saving edit
    };
  },
  mounted() {
    this.fetchTheatres();
  },
  methods: {
    async fetchTheatres() {
      try {
        const response = await fetch('http://127.0.0.1:5000/gettheatres', {
          headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
        });
        if (!response.ok) {
          throw new Error('Failed to fetch theatres');
        }
        const data = await response.json(); // Parse the response data as JSON
        this.theatres = data.reverse();
        this.loading = false;
      } catch (error) {
        this.error = 'Error fetching theaters. Please try again later.';
        console.error(error);
        this.loading = false;
      }
    },
    addShow(theatre) {
      
      this.$router.push({ name: 'showpage', params: { theatreid: theatre.id } });
    },
    toggleEdit(theatre) {
      // Toggle the editing mode for the selected theatre
      theatre.editing = !theatre.editing;
    },
    async saveEdit(theatre) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/edittheatre/${theatre.id}`, {
          method: 'PUT',
          headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        'Content-Type': 'application/json', // Set the content type header
      },
          body: JSON.stringify({ name: theatre.name }),
        });

        if (response.ok) {
          // Update the theatre name and toggle editing mode
          theatre.editing = false;
          this.successMessage = 'Theatre name updated successfully!';
          this.errorMessage = ''; // Clear error message
        } else {
          this.successMessage = ''; // Clear success message
          this.errorMessage = 'Failed to save theatre edit';
        }
      } catch (error) {
        this.successMessage = ''; // Clear success message
        this.errorMessage = 'Error saving theatre edit';
        console.error('Error saving theatre edit:', error);
      }
    },
    async deleteTheatre(theatreId) {
      const confirmation = window.confirm('Are you sure you want to delete this theatre?');
      if (confirmation) {
        try {
          const response = await fetch(`http://127.0.0.1:5000/deletetheatre/${theatreId}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          }});

          if (response.ok) {
            // Remove the deleted theatre from the list
            this.theatres = this.theatres.filter(theatre => theatre.id !== theatreId);
          } else {
            console.error('Failed to delete theatre');
          }
        } catch (error) {
          console.error('Error deleting theatre:', error);
        }
      }
    },
  },
};
</script>

<style>
@import '~bootstrap/dist/css/bootstrap.min.css';
</style>
