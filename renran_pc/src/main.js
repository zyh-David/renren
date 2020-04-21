// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import settings from "./settings"
import axios from 'axios'

Vue.prototype.$settings = settings;
Vue.config.productionTip = false

// elementUI 导入
import ElementUI from 'element-ui';
import "element-ui/lib/theme-chalk/index.css";
// 全局初始化样式
import "../static/css/reset.css";

import mavonEditor from 'mavon-editor'
import 'mavon-editor/dist/css/index.css'
// 注册mavon-editor组件
Vue.use(mavonEditor);
new Vue({
    'el': '#main'
});

// iconfont字体
import "../static/css/iconfont.css";
import "../static/css/iconfont.eot";
// 调用插件
Vue.use(ElementUI);

// 初始化axios
// 允许ajax发送请求时附带cookie
axios.defaults.withCredentials = false;
Vue.prototype.$axios = axios; // 把对象挂载vue中

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
