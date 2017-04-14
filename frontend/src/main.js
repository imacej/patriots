import Vue from 'vue';
import App from './App';
import router from './router';
import ElementUI from 'element-ui';
import axios from 'axios'; // 引入 Axios 库
import VueAxios from 'vue-axios';
import 'element-ui/lib/theme-default/index.css'; // 默认主题
// import '../static/css/theme-green/index.css';       // 浅绿色主题

//开启debug模式
Vue.config.debug = true;

global.API_ROOT = "http://127.0.0.1:12333/v1/"

Vue.use(VueAxios, axios);
Vue.use(ElementUI);
new Vue({
    router,
    render: h => h(App)
}).$mount('#app');