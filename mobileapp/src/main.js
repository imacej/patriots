// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import FastClick from 'fastclick'
import VueRouter from 'vue-router'
import router from './router';
import App from './App'

Vue.use(VueRouter)

FastClick.attach(document.body)

/* eslint-disable no-new */
new Vue({
    router,
    render: h => h(App)
}).$mount('#app')