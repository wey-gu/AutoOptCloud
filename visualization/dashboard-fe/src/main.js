import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'
import VueSocketIO from 'vue-socket.io'
import store from './store'
import VueRouter from 'vue-router'
import Dashboard from './components/Dashboard'
import DataTable from './components/DataTable'
import config from './config'

Vue.config.productionTip = false
Vue.use(VueRouter)
Vue.use(new VueSocketIO({
  debug: true,
  connection: config.backendURL,
  vuex: {
      store,
      actionPrefix: 'SOCKET_',
      mutationPrefix: 'SOCKET_'
  }
}))

const routes = [
  { path: '/', component: Dashboard },
  { path: '/data', component: DataTable },
]

const router = new VueRouter({
  mode: 'history',
  routes // routes: routes
})

new Vue({
  store,
  router,
  render: h => h(App)
}).$mount('#app')
