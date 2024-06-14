<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <p>
      Bitte klicken Sie hier, um Ihre persönliche Wetterprognose zu erhalten.<br>
      <button @click="fetchWeather">Wetterdaten berechnen</button><br>
      <span class="weather-output" v-html="weatherOutput"></span>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const lat = ref(0);
const lng = ref(0);
const token = ref(null); // Variable zum Speichern des Tokens
const weatherOutput = ref(''); // Reactive variable for weather output

const msg = 'Willkommen zu Ihrer Wetter-App';

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
      password: "admin"
    }, {
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
    weatherOutput.value = data.message.replace(/\n/g, '<br>'); // Replace \n with <br>
  } catch (error) {
    weatherOutput.value = error.message.replace(/\n/g, '<br>'); // Replace \n with <br>
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
body {
  font-family: 'Arial', sans-serif;
  background-color: #f4f4f9;
  color: #333;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  margin: 0;
}

.hello {
  background: #fff;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

h1 {
  color: #333;
  margin-bottom: 1.5rem;
}

p {
  font-size: 1.2rem;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

button {
  background-color: #CEDDEF;
  color: #2c3e50;
  border: none;
  padding: 10px 20px;
  text-align: center;
  font-size: 1rem;
  margin: 1rem 0;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #ceddef9c;
}

.weather-output {
  padding: 10px;
  margin: 10px;
  max-width: 500px;
  display: inline-block;
  background: #f0f0f0;
  border-radius: 4px;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
  font-size: 1.1rem;
  color: #555;
  text-align: left;
}

a {
  color: #CEDDEF;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>

