<template>
  <div>
    <Header />

    <div class="container mt-4">
      <h2>Add Show</h2>

      <!-- Success alert for show added -->
      <div v-if="showAddedSuccess" class="alert alert-success" role="alert">
        Show added successfully!
      </div>

      <!-- Error alert for show add failure -->
      <div v-if="showAddedError" class="alert alert-danger" role="alert">
        Error adding show. Please try again.
      </div>

      <div v-if="showFormVisible" class="mb-4">
        <form @submit.prevent="createShow">
          <div class="mb-3">
            <label for="name" class="form-label">Name:</label>
            <input type="text" id="name" v-model="show.name" class="form-control" required>
          </div>
          <div class="mb-3">
            <label for="rating" class="form-label">Rating:</label>
            <input type="number" id="rating" v-model="show.rating" min="1" max="5" step="0.1" class="form-control" required>
          </div>
          <div class="mb-3">
            <label>Genres:</label>
            <div v-for="genre in genres" :key="genre.value" class="form-check form-check-inline">
              <input type="checkbox" :id="genre.value" :value="genre.value" v-model="show.genres" class="form-check-input">
              <label :for="genre.value" class="form-check-label">{{ genre.label }}</label>
            </div>
          </div>
          <div class="mb-3">
            <label for="ticket_price" class="form-label">Ticket Price:</label>
            <input type="number" id="ticket_price" v-model="show.ticket_price" class="form-control" required>
          </div>
          <div>
            <button type="submit" class="btn btn-primary">Add Show</button>
          </div>
        </form>
      </div>
    </div>
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
      showFormVisible: true,
      show: {
        name: '',
        rating: 0,
        genres: [],
        ticket_price: 0,
      },
      showAddedSuccess: false,
      showAddedError: false,
      genres: [
        { label: 'Comedy', value: 'comedy' },
        { label: 'Action', value: 'action' },
        { label: 'Sci-Fi', value: 'scifi' },
        { label: 'Romance', value: 'romance' },
        { label: 'Horror', value: 'horror' },
        { label: 'Drama', value: 'drama' },
        { label: 'Fantasy', value: 'fantasy' },
      ],
    };
  },
  methods: {
    async createShow() {
      const theatreid = this.$route.params.theatreid;
      try {
        const response = await fetch(`http://127.0.0.1:5000/admin/theatres/${theatreid}/add_show`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          },
          body: JSON.stringify(this.show),
        });

        if (!response.ok) {
          throw new Error('Failed to add show');
        }

        this.showAddedSuccess = true;
        setTimeout(() => {
          this.showAddedSuccess = false;
        }, 3000);
      } catch (error) {
        console.error(error);
        this.showAddedError = true;
        setTimeout(() => {
          this.showAddedError = false;
        }, 3000);
      }
    },
  },
};
</script>
