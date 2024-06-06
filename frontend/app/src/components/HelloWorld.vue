<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <p>Bitte klicken Sie hier um ihre persönliche Wetterprognose zu erhalten Test.<br>
      <button @click="Callbackend()">Wetterdaten berechnen</button><br>
      {{ lat }} , {{ lng }} , {{ outputElement }}
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

function Callbackend(){
  // get location of user
  getLocation()

  // Define the API URL
  const apiUrl = `http://ec2-44-194-144-99.compute-1.amazonaws.com:5000/weather/lookup?lattitude=${lat.value}&longitude=${lng.value}`
  const outputElement = document.getElementById('output');

  fetch(apiUrl)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      // Display data in an HTML element
      outputElement.textContent = JSON.stringify(data, null, 2);
    })
    .catch(error => {
      console.error('Error:', error);
    });
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
