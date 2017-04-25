// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import FastClick from 'fastclick';
import VueRouter from 'vue-router';
import Vuex from 'vuex';
import router from './router';
// 项目结构 https://vuex.vuejs.org/zh-cn/structure.html
// import store from './store'
import App from './App';

Vue.use(VueRouter);
Vue.use(Vuex);

FastClick.attach(document.body);

const store = new Vuex.Store({
    state: {
        tabIndex: 0
    },
    mutations: {
        changeTab(state, index) {
            state.tabIndex = index
        }
    }
})

/* eslint-disable no-new */
new Vue({
    store,
    router,
    render: h => h(App)
}).$mount('#app')