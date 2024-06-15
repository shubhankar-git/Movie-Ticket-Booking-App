<template>
    <div>
      <Header />
      <h2>My Booked Tickets</h2>
      <div v-if="bookedTickets.length > 0">
        <ul>
          <li v-for="(ticket, index) in bookedTickets" :key="index">
            <p><strong>Show Name:</strong> {{ ticket.show_name }}</p>
            <p><strong>Number of Tickets:</strong> {{ ticket.num_tickets }}</p>
            <p><strong>Total Price:</strong> ${{ ticket.total_price }}</p>
            <hr>
          </li>
        </ul>
      </div>
      <div v-else>
        <p>No booked tickets found.</p>
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
        bookedTickets: [], // Store the booked tickets of the user
      
      };
    },
    created() {
      this.fetchBookedTickets();
    },
    methods: {
      async fetchBookedTickets() {
        
        try {
          const response = await fetch("http://127.0.0.1:5000/user/booked-tickets", {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          });
  
          if (!response.ok) {
            throw new Error("Failed to fetch booked tickets");
          }
  
          const data = await response.json();
          this.bookedTickets = data.reverse();
        } catch (error) {
          console.error(error);
        }
      },
      
    },
  };
  </script>
  