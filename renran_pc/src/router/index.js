import Vue from 'vue'
import Router from 'vue-router'
import Home from "../components/Home";
import Login from "../components/Login";
import Register from "../components/Register";
import FindPassword from "../components/FindPassword";
import ResetPassword from "../components/ResetPassword";
import Write from "../components/Write";
import Writed from "../components/Writed";
import Article from "../components/Article";

Vue.use(Router);

export default new Router({
  mode:'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/home',
      name: 'Home',
      component: Home
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
    },
     {
      name:"Register",
      path: "/register",
      component:Register,
    },
    {
      name:"find_password",
      path: "/find_password",
      component:FindPassword,
    },
    {
      name:"reset_password",
      path: "/reset_password",
      component:ResetPassword,
    },
    {
       name:"Write",
       path:"/write",
       component: Write,
     },
    {
       name:"Writed",
       path:"/:id/writed",
       component: Writed,
     },
    {
       name:"Article",
       path:"/article/:id",
       component: Article,
     },
  ]
})
