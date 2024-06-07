<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <p>Bitte klicken Sie hier um ihre persönliche Wetterprognose zu erhalten Test.<br>
      <button @click="async() => await fetchWeather()">Wetterdaten berechnen</button><br>
      {{ lat }} , {{ lng }} , <span id="weatherOutput"></span>
    </p>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  }
}
</script>

<script setup>

import {ref} from 'vue'

const lat = ref(0)
const lng = ref(0)

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition((position) => {
      lat.value = position.coords.latitude
      lng.value = position.coords.longitude
    })
  }
}

async function fetchWeather() {
  const outputElement = document.getElementById('weatherOutput');

  try {
    getLocation()
    const apiUrl = `http://localhost:8010/weather/lookup?lattitude=${lat.value}&longitude=${lng.value}`
    const response = await fetch(apiUrl, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        },
        mode: 'no-cors'
    });

    if (!response.ok) {
        throw new Error(response.statusText);
    }

    const data = await response.json();
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
