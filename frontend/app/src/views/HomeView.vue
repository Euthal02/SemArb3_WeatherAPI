<template>
  <div class="home">
    <img alt="Wetter API Logo" src="../assets/WeatherAPI_Logo.png">
    <HelloWorld msg="Willkommen bei unserer WetterAPI App"/>
    <h1>Willkommen bei unserer WetterAPI App</h1>
    <p>
      Bitte klicken Sie hier um ihre persönliche Wetterprognose zu erhalten.<br>
      <button @click="getLocation()">Wetterdaten berechnen</button><br>
      {{ lat }} , {{ lng }}
    </p>
  </div>
</template>

<script>

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

</script>
