<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <p>
      Bitte klicken Sie hier um ihre persönliche Wetterprognose zu erhalten.<br>
      <button @click="">Wetterdaten berechnen</button>
    </p>
  </div>
</template>


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

</script>


<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: String
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
