import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Vue3Geolocation from 'vue3-geolocation';


app.use(VueGeolocation);
createApp(App).use(router).mount('#app')


