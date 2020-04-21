export default {
  Host:"http://api.renran.cn:8000",
  TC_captcha:{
    app_id:'2039770737',
  },
  get_login_user(){
    let ret = localStorage.user_token || sessionStorage.user_token;
    return ret
  }
}
