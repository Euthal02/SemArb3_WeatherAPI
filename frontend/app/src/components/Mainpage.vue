<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <p>
      Bitte klicken Sie hier, um Ihre persönliche Wetterprognose zu erhalten.<br>
      <button @click="fetchWeather" :disabled="loading">Wetterdaten berechnen</button><br>
      <div v-if="loading" class="loading-bar"></div> <!-- Ladebalken -->
      <span class="weather-output" v-html="weatherOutput"></span> <!-- Wetterausgabe -->
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const lat = ref(0); // Latitude (Breitengrad)
const lng = ref(0); // Longitude (Längengrad)
const token = ref(null); // Variable zum Speichern des Tokens
const weatherOutput = ref(''); // Reaktive Variable für die Wetterausgabe
const loading = ref(false); // Reaktive Variable für den Ladezustand

const msg = 'Willkommen zu Ihrer Wetter-App';

async function getLocation() {
  // Funktion zur Ermittlung der aktuellen Geoposition
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
  // Funktion zur Authentifizierung und Token-Erhalt
  try {
    const response = await axios.post('https://backend.meuthak.ch/users/login', {
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
  // Funktion zum Abrufen der Wetterdaten
  loading.value = true; // Ladezustand auf true setzen
  try {
    const accessToken = await testGetUsersWithAuthentication(); // Authentifizierung durchführen und Token erhalten

    let latitude;
    let longitude;
    try {
      const geo_values = await getLocation(); // Geoposition ermitteln
      latitude = geo_values[0];
      longitude = geo_values[1];
      console.log(`Latitude: ${latitude}, Longitude: ${longitude}`);
    } catch (error) {
      console.error('Error getting location:', error);
    }

    const apiUrl = `https://backend.meuthak.ch/weather/lookup?lattitude=${latitude}&longitude=${longitude}`;

    const response = await axios.get(apiUrl, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
        'Access-Control-Allow-Origin': '*'
      }
    });

    const data = response.data;
    console.log(data);
    weatherOutput.value = data.message.replace(/\n/g, '<br>'); // Zeilenumbrüche ersetzen
  } catch (error) {
    weatherOutput.value = error.message.replace(/\n/g, '<br>'); // Zeilenumbrüche ersetzen
  } finally {
    loading.value = false; // Ladezustand wieder auf false setzen
  }
}
</script>

<style scoped>
/* CSS für den Ladebalken */
.loading-bar {
  width: 100%;
  height: 4px;
  background-color: #CEDDEF;
  margin: 10px 0;
  animation: loading 1s linear infinite;
}

@keyframes loading {
  0% { width: 0%; }
  100% { width: 100%; }
}

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
  width: 100%;
  max-width: 600px;
  box-sizing: border-box;
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
  margin: 10px auto;
  max-width: 100%;
  display: inline-block;
  background: #f0f0f0;
  border-radius: 4px;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
  font-size: 1.1rem;
  color: #555;
  text-align: left;
  word-wrap: break-word;
}

a {
  color: #CEDDEF;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

/* Responsive Anpassungen */
@media (max-width: 600px) {
  .hello {
    padding: 1rem;
  }

  p {
    font-size: 1rem;
  }

  button {
    width: 100%;
    padding: 10px;
  }

  .weather-output {
    font-size: 1rem;
  }
}
</style>
