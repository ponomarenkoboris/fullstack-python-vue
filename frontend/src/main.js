import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'

Vue.config.productionTip = false
/* TODO устранить ошибки:
* serviceworker.js:47 Uncaught (in promise) TypeError: Failed to execute 'put' on 'Cache': Request method 'DELETE' is unsupported at networkFirst (serviceworker.js:47)
* serviceworker.js:47 Uncaught (in promise) TypeError: Failed to execute 'put' on 'Cache': Request method 'POST' is unsupported at networkFirst (serviceworker.js:47)
* serviceworker.js:47 Uncaught (in promise) TypeError: Failed to execute 'put' on 'Cache': Request method 'PUT' is unsupported at networkFirst (serviceworker.js:47)
* */
new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')
