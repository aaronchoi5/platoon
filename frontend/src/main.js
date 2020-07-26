import Vue from 'vue'
import App from './App.vue'
import router from './router'
import socketio from 'socket.io'
import store from "./store"

Vue.config.productionTip = false

new Vue({
  store,
  router,
  render: h => h(App)
}).$mount('#app')
