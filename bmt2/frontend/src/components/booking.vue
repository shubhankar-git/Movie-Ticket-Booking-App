<template>
  <div>
    <Header />
    <div class="container mt-4">
      <h2 class="mb-3">Booking Page</h2>
      <div v-if="show" class="card">
        <div class="card-body">
          <h3 class="card-title">{{ show.name }}</h3>
          <p class="card-text">Rating: {{ show.rating }}</p>
          <p class="card-text">Genres: {{ show.genres.join(', ') }}</p>
          <p class="card-text">Ticket Price: ${{ show.ticket_price }}</p>
          <p class="card-text">Available Seats: {{ show.available_seats }}</p>
          <p v-if="show.is_house_full" class="text-danger">House Full!</p>
          <label for="numTickets">Number of Tickets:</label>
          <input type="number" id="numTickets" class="form-control" v-model.number="numTickets" :max="show.available_seats" :disabled="show.is_house_full">
          <p v-if="numTickets > 0" class="mt-2">Price per Ticket: ${{ show.ticket_price }}</p>
          <p v-if="numTickets > 0">Total Price: ${{ numTickets * show.ticket_price }}</p>
          <button @click="bookTickets" class="btn btn-primary" :disabled="numTickets <= 0 || show.is_house_full">Book Tickets</button>
        </div>
      </div>
      <div v-else>
        <p>Loading show details...</p>
      </div>

      <!-- Bootstrap Alert -->
      <div v-if="alertMessage" class="alert alert-dismissible fade show mt-3" :class="['alert', alertType]">
        {{ alertMessage }}
        <button type="button" class="close" @click="closeAlert">
          <span>&times;</span>
        </button>
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
      show: null,
      numTickets: 0,
      alertMessage: '',
      alertType: ''
    };
  },
  async created() {
    // Fetch the show details based on showId from the route parameters
    const showId = this.$route.params.showId;
    this.fetchShowData(showId);
  },
  methods: {
    async fetchShowData(showId) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/bookings/${showId}`, {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          },
        });

        if (!response.ok) {
          throw new Error('Failed to fetch show data');
        }

        const data = await response.json();
        this.show = data;
      } catch (error) {
        console.error(error);
      }
    },
    async bookTickets() {
      try {
        // Make a POST request to the backend to book the tickets
        const response = await fetch(`http://127.0.0.1:5000/bookings/${this.show.id}`, {
          method: 'POST', 
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          },
          body: JSON.stringify({
            numTickets: this.numTickets,
          })
        });
        
        if (response.ok) {
          this.showAlert('Tickets booked successfully!', 'alert-success');
          this.fetchShowData(this.show.id);
          
        } else {
          throw new Error('Failed to book tickets');
        }
      } catch (error) {
        console.error(error);
        this.showAlert('Failed to book tickets', 'alert-danger');
      }
    },
    showAlert(message, type) {
      this.alertMessage = message;
      this.alertType = type;
      setTimeout(this.closeAlert, 3000); // Close after 3 seconds
    },
    closeAlert() {
      this.alertMessage = '';
      this.alertType = '';
    },
  },
};
</script>
