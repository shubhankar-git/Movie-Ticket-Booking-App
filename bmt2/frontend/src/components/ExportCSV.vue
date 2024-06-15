
<template>
  <div>
    <Header />
    <h1>Theatre CSV Export</h1>
    <form @submit.prevent="exportCSV">
      <label for="theatreId">Select Theatre:</label>
      <select v-model="selectedTheatre" required>
        <option v-for="theatre in theatres" :key="theatre.id" :value="theatre.id">{{ theatre.name }} ID:{{ theatre.id }}</option>
      </select>
      <button type="submit">Export CSV</button>
    </form>
    <p v-if="exporting">Export in progress...</p>
    <p v-if="exportedFile">{{ exportedFile }}</p>
    <p v-if="downloadLink">
      <a :href="downloadLink" download>Download CSV</a>
    </p>
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
      selectedTheatre: null,
      exporting: false,
      exportedFile: null,
      downloadLink: null, // Store download link for the CSV file
      theatres: [], // Add theatre data here
    };
  },
  methods: {
    async fetchTheatres() {
      try {
        const response = await fetch('http://127.0.0.1:5000/exportTheatres', {
          method: 'GET',
          headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
        });
        
        if (response.ok) {
          const data = await response.json();
          this.theatres = data;
        } else {
          console.error('Failed to fetch theatre data');
        }
      } catch (error) {
        console.error('Error fetching theatre data:', error);
      }
    },
    async exportCSV() {
      if (!this.selectedTheatre) {
        return;
      }

      this.exporting = true;
      const response = await fetch(`http://127.0.0.1:5000/export-csv/${this.selectedTheatre}`, {
        method: 'GET',
        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
      });

      if (response.ok) {
        const data = await response.json();
        console.log(data);
        this.exportedFile = data.message;
        this.downloadLink = data.download_link; // Set the download link
        alert('CSV export completed!');
      } else {
        console.error('Failed to export CSV');
      }

      this.exporting = false;
    },
    async fetchDownloadLink() {
      if (!this.exportedFile) {
        return;
      }

      this.fetchingDownloadLink = true;
      try {
        const response = await fetch(`http://127.0.0.1:5000/download-csv/${this.selectedTheatre}`, {
          method: 'GET',
          headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
        });

        if (response.ok) {
    try {
        const blob = await response.blob();
        const objectURL = URL.createObjectURL(blob);
        
        // Get the filename from the exportedFile message
        const filename = this.exportedFile;

        this.downloadLink = objectURL;
        this.downloadFilename = filename;

        alert('CSV export completed!');
    } catch (error) {
        console.error('Error creating Blob:', error);
    }
} else {
    console.error('Failed to export CSV');
}

      } catch (error) {
        console.error('Error fetching download link:', error);
      }

      this.fetchingDownloadLink = false;
    },
  },

  watch: {
    exportedFile: 'fetchDownloadLink', // Automatically fetch download link when exportedFile changes
  },
  
  mounted() {
    this.fetchTheatres();
  },
};
</script>
