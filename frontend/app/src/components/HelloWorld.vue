<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <p>Bitte klicken Sie hier, um Ihre persönliche Wetterprognose zu erhalten.<br>
      <button @click="async () => await fetchWeather()">Wetterdaten berechnen</button><br>
      {{ lat }}, {{ lng }}, <span id="weatherOutput"></span>
    </p>
    <div v-if="token">
      <p>Token: {{ token }}</p>
    </div>
  </div>
</template>

<script setup>

import { ref } from 'vue'
import axios from 'axios'

const lat = ref(0)
const lng = ref(0)
const token = ref(null); // Variable zum Speichern des Tokens


async function getLocation() {
  return new Promise((resolve, reject) => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          lat.value = position.coords.latitude;
          lng.value = position.coords.longitude;
          resolve([position.coords.latitude, position.coords.longitude]);
        },
        (error) => {
          reject(error);
        }
      );
    } else {
      reject(new Error("Geolocation is not supported by this browser."));
    }
  });
}

async function testGetUsersWithAuthentication() {
    try {
        const response = await axios.post('http://localhost:5000/users/login', {
            email: "admin@admin.ch",
            password: "admin"}, {
          headers: {
              'Access-Control-Allow-Origin': '*'
           }
        });

        if (!response.data.token) {
            throw new Error('Failed to obtain token');
        }

        const accessToken = response.data.token;
        token.value = accessToken; 
        return accessToken;
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}

async function fetchWeather() {
  const outputElement = document.getElementById('weatherOutput');
  try {
    const accessToken = await testGetUsersWithAuthentication(); // Authentifizierung durchführen und Token erhalten

    let latitude;
    let longitude;
    try {
      const geo_values = await getLocation();
      latitude = geo_values[0];
      longitude = geo_values[1];
      console.log(`Latitude: ${latitude}, Longitude: ${longitude}`);
    } catch (error) {
      console.error('Error getting location:', error);
    }

    const apiUrl = `http://localhost:5000/weather/lookup?lattitude=${latitude}&longitude=${longitude}`;
    
    const response = await axios.get(apiUrl, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
        'Access-Control-Allow-Origin': '*'
      }
    });

    const data = response.data;
    console.log(data);
    outputElement.textContent = data.message;
  } catch (error) {
    outputElement.textContent = error.message;
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #CEDDEF;
}
</style>
