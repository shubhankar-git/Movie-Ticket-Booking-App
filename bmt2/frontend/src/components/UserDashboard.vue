<template>
  <div class="container mt-5">
    <Header />
    <h2>User Dashboard</h2>
    
    
    <!-- Search input field -->
    <input v-model="searchQuery" type="text" placeholder="Search by name or place">
    
    <!-- Search button -->
    <button @click="searchTheatres">{{ isSearching ? 'Clear' : 'Search' }}</button>
    
    <label>
      <input type="radio" v-model="searchIn" value="theatres">
      Search in Theatres
    </label>
    <label>
      <input type="radio" v-model="searchIn" value="shows">
      Search in Shows
    </label>
    
    <div v-if="filteredTheatres.length === 0 && searchIn === 'theatres'">
      <p>No results found.</p>
    </div>

    <div v-for="theatre in theatres" :key="theatre.id" class="card mb-3">
      <div class="card-header">{{ theatre.name }}</div>
      <div class="card-body">
        <p class="card-text">Location: {{ theatre.place }}</p>
        <p class="card-text">Capacity: {{ theatre.capacity }}</p>
        <template v-if="isSearching && searchIn === 'shows'">
          <p class="card-text">Number of matching shows: {{ theatre.shows.length }}</p>
        </template>
        <button @click="toggleMovies(theatre.id)" class="btn btn-primary">
          {{ theatre.showMovies ? "Hide Movies" : "Show Movies" }}
        </button>

        <div v-if="theatre.showMovies">
          <div v-for="show in theatre.shows" :key="show.id" class="card mb-2">
            <div class="card-body">
              <h5 class="card-title">{{ show.name }}</h5>
              <p class="card-text">Rating: {{ show.rating }}</p>
              <p class="card-text">Genres: {{ show.genres.join(', ') }}</p>
              <p class="card-text">Ticket Price: ${{ show.ticket_price }}</p>
              <p class="card-text">Available Seats: {{ show.available_seats }}</p>
              <p v-if="show.is_house_full">House Full!</p>
              <button v-else @click="bookShow(theatre.id, show.id)" :disabled="show.available_seats === 0" class="btn btn-success">
                Book Now
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Header from './Header.vue';
export default {
  components: {
    Header,
  },
  
  data() {
return {
  theatres: [],
  originalTheatres: [],
  searchQuery: "",
  isSearching: false,
  searchIn: "theatres", // Default option is to search in theatres
};
  },
  computed: {
  filteredTheatres() {
    const query = this.searchQuery.toLowerCase().trim();
    if (!query) return this.theatres;
    return this.theatres.filter(
      (theatre) =>
        theatre.name.toLowerCase().includes(query) ||
        theatre.place.toLowerCase().includes(query)
    );
  },
},
mounted() {
  this.fetchTheatresData();
},


  methods: {
    async fetchTheatresData() {
      try {
        const response = await fetch('http://127.0.0.1:5000/user/dashboard', {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          },
        });
       
        if (!response.ok) {
          throw new Error('Failed to fetch theatre data');
        }

        const data = await response.json();
        this.originalTheatres = data.reverse();
        this.theatres = data.map(theatre => ({ ...theatre, showMovies: false })); // Add showMovies property
      } catch (error) {
        console.error(error);
      }
  },
 
    async bookShow(theatreId, showId) {
      this.$router.push({ name: 'booking', params: { theatreId, showId } });
    },
    toggleMovies(theatreId) {
      // Method to toggle showMovies property for a specific theatre
      this.theatres = this.theatres.map(theatre =>
        theatre.id === theatreId ? { ...theatre, showMovies: !theatre.showMovies } : theatre
      );
    },
    searchTheatres() {
      if (!this.isSearching) {
      // First click on Search, perform filtering
      this.isSearching = true;
      const query = this.searchQuery.trim().toLowerCase();
      this.theatres = this.filterTheatres(query);
       } else {
      // Second click on Search, clear the search and show all data
      this.isSearching = false;
      this.searchQuery = "";
      this.theatres = this.searchIn === "theatres" ? this.originalTheatres : this.filterTheatres("");
    }
    },
    filterTheatres(query) {    const lowerCaseQuery = query.toLowerCase().trim();
    if (this.searchIn === "theatres") {
      // Filter based on theatre name or place
      return this.originalTheatres.filter((theatre) => {
        return (
          theatre.name.toLowerCase().includes(lowerCaseQuery) ||
          theatre.place.toLowerCase().includes(lowerCaseQuery)
        );
      });
    } else if (this.searchIn === "shows") {
      // Filter based on show name, genres, or rating
      return this.originalTheatres.map((theatre) => {
        const filteredShows = theatre.shows.filter((show) => {
          return (
            show.name.toLowerCase().includes(lowerCaseQuery) ||
            show.genres.some((genre) => genre.toLowerCase().includes(lowerCaseQuery)) ||
            show.rating.toString().includes(lowerCaseQuery)
          );
        });
        return {
          ...theatre,
          shows: filteredShows,
        };
      });
    }
    },

  },
};
</script>
