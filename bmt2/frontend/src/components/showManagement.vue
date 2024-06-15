<template>
  <div class="container mt-4">
    <Header />
    <h2 class="mb-4">Show Management</h2>

    <!-- Success alert for show edited -->
    <div v-if="showEditedSuccess" class="alert alert-success" role="alert">
      Show edited successfully!
    </div>

    <!-- Error alert for show edit failure -->
    <div v-if="showEditedError" class="alert alert-danger" role="alert">
      Error editing show. Please try again.
    </div>

    <!-- Success alert for show deleted -->
    <div v-if="showDeletedSuccess" class="alert alert-success" role="alert">
      Show deleted successfully!
    </div>

    <!-- Error alert for show delete failure -->
    <div v-if="showDeletedError" class="alert alert-danger" role="alert">
      Error deleting show. Please try again.
    </div>

    <div v-for="(theatre, theatreId) in theatres" :key="theatreId" class="mb-4">
      <h3>{{ theatre.name }}</h3>
      <div v-for="show in theatre.shows" :key="show.id">
        <div class="mb-2">
          <strong>Show Name:</strong>
          <template v-if="show.editing">
            <input class="form-control" v-model="show.name" />
          </template>
          <template v-else>
            {{ show.name }}
          </template>
        </div>
        <div class="mb-2">
          <strong>Rating:</strong>
          <template v-if="show.editing">
            <input class="form-control" v-model="show.rating" />
          </template>
          <template v-else>
            {{ show.rating }}
          </template>
        </div>
        <div class="mb-2">
          <strong>Genres:</strong>
          <template v-if="show.editing">
            <div v-for="genre in genres" :key="genre.value" class="form-check form-check-inline">
              <input type="checkbox" :id="genre.value" :value="genre.value" v-model="show.genres" :checked="show.genres.includes(genre.value)">
              <label :for="genre.value" class="form-check-label"
                :class="{ 'text-primary': show.genres.includes(genre.value) }">
                {{ genre.label }}
              </label>
            </div>
          </template>
          <template v-else>
            {{ show.genres.join(',') }}
          </template>
        </div>
        <div class="mb-2">
          <strong>Ticket Price:</strong>
          <template v-if="show.editing">
            <input class="form-control" v-model="show.ticket_price" />
          </template>
          <template v-else>
            {{ show.ticket_price }}
          </template>
        </div>
        <button class="btn btn-primary mr-2" @click="toggleEdit(show)">
          {{ show.editing ? 'Cancel Edit' : 'Edit' }}
        </button>
        <button class="btn btn-success mr-2" @click="saveEdit(show)" v-if="show.editing">Save</button>
        <button class="btn btn-danger" @click="deleteShow(show)">Delete</button>
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
      theatres: {},
      showEditedSuccess: false,
      showEditedError: false,
      showDeletedSuccess: false,
      showDeletedError: false,
      genres: [
        { label: 'Comedy', value: 'Comedy' },
        { label: 'Action', value: 'Action' },
        { label: 'Sci-Fi', value: 'Sci-Fi' },
        { label: 'Romance', value: 'Romance' },
        { label: 'Horror', value: 'Horror' },
        { label: 'Drama', value: 'Drama' },
        { label: 'Fantasy', value: 'Fantasy' },
      ],
    };
  },
  methods: {
    async fetchShows() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/getshows', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
        });

        if (response.status === 200) {
          this.theatres = response.data;
          this.theatres.reverse();
        } else {
          console.error('Failed to fetch shows');
        }
      } catch (error) {
        console.error('Error fetching shows:', error);
      }
    },
    async toggleEdit(show) {
      show.editing = !show.editing;
    },
    async saveEdit(show) {
      try {
        const editedGenres = this.genres.filter(genre => show.genres.includes(genre.value)).map(genre => genre.value);
        const response = await axios.put(
          `http://127.0.0.1:5000/editshow/${show.id}`,

          {
            name: show.name,
            rating: show.rating,
            genres: editedGenres,
            ticket_price: show.ticket_price,
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            },
          }
        );

        if (response.status === 200) {
          this.showEditedSuccess = true;
          await this.fetchShows();

          setTimeout(() => {
            this.showEditedSuccess = false;
          }, 3000);
        } else {
          this.showEditedError = true;
          setTimeout(() => {
            this.showEditedError = false;
          }, 3000);
        }
      } catch (error) {
        console.error('Error editing show:', error);
        this.showEditedSuccess = false;
        this.showEditedError = true;
        setTimeout(() => {
          this.showEditedError = false;
        }, 3000);
      }
    },
    async deleteShow(show) {
      const confirmation = window.confirm('Are you sure you want to delete this show?');
      if (confirmation) {
        try {
          const response = await axios.delete(
            `http://127.0.0.1:5000/deleteshow/${show.id}`,
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem('access_token')}`,
              },
            }
          );

          if (response.status === 200) {
            this.showDeletedSuccess = true;
            await this.fetchShows();

            setTimeout(() => {
              this.showDeletedSuccess = false;
            }, 3000);
          } else {
            this.showDeletedError = true;
            setTimeout(() => {
              this.showDeletedError = false;
            }, 3000);
          }
        } catch (error) {
          console.error('Error deleting show:', error);
          this.showDeletedSuccess = false;
          this.showDeletedError = true;
          setTimeout(() => {
            this.showDeletedError = false;
          }, 3000);
        }
      }
    },
  },
  mounted() {
    this.fetchShows();
  },
};
</script>
