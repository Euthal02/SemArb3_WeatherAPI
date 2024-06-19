<template>
  <div class="home">
    <img alt="Wetter API Logo" src="../assets/WeatherAPI_Logo.png">
    <HelloWorld msg="Willkommen bei unserer WetterAPI App"/>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'HomeView',
  components: {
    HelloWorld
  }
}
</script>
