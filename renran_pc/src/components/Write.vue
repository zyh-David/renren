<template>
  <div class="write">
    <div class="_2v5v5">
      <div class="_3zibT"><a href="/">回首页</a></div>
      <div class="_1iZMb">
        <div class="_33Zlg" @click="collection_form=true"><i class="fa fa-plus"></i><span>新建文集</span></div>
        <div class="_2G97m">
          <form class="M8J6Q" :class="collection_form?'_2a1Rp':'_1mU5v'">
            <input type="text" placeholder="请输入文集名..." v-model="collection_name" class="_1CtV4">
            <button type="submit" @click.prevent="add_collection" class="dwU8Q _3zXcJ _3QfkW"><span>提 交</span></button>
            <button type="button" class="vIzwB _3zXcJ" @click="collection_form=false"><span>取 消</span></button>
          </form>
        </div>
      </div>
      <ul class="_3MbJ4 _3t059">
        <li class="_3DM7w" :class="current_collection===key?'_31PCv':''" :title="collection.name" v-for="collection,key in collection_list" @click="current_collection=key">
          <div class="_3P4JX _2VLy-" @click="current_collection=key;is_click=is_click==false?true:false;">
            <i class="fa fa-gear"></i>
            <span>
              <ul class="_2V8zt _3FcHm _2w9pn" :class="current_collection===key && is_click===true?'NvfK4':''" >
                <li class="_2po2r cRfUr" title="">
                  <el-button type="text" @click="edit_collection(collection)"><i class="fa fa-pencil-square-o"></i>修改文集</el-button>
                </li>
                <li class="_2po2r cRfUr" title="">
                  <span class=""><i class="fa fa-trash-o"></i>删除文集</span>
                </li>
              </ul>
            </span>
          </div>
          <span>{{collection.name}}</span>
        </li>

      </ul>
      <div style="height: 50px;"></div>
      <div role="button" class="h-5Am">
        <span class="ant-dropdown-trigger"><i class="fa fa-bars"></i><span>设置</span></span>
        <span class="Yv5Zx">遇到问题<i class="fa fa-question-circle-o"></i></span>
      </div>
    </div>
    <div class="rQQG7">
      <div class="_3revO _2mnPN">
        <div class="_3br9T">
          <div>
            <div class="_1GsW5" @click="add_article('insert')"><i class="fa fa-plus-circle"></i><span>新建文章</span></div>
            <ul class="_2TxA-">
              <li class="_25Ilv" :class="current_acticle==key?'_33nt7':''" @click="current_acticle=key" :title="article.title" v-for="article,key in article_list">
                <i class="_13kgp _2m93u"></i>
                <div class="_3P4JX poOXI" @click="current_acticle=key;is_click_acticle=is_click_acticle==false?true:false">
                  <i class="fa fa-gear"></i>
                  <span>
                    <ul class="_2V8zt _3FcHm _2w9pn" :class="current_acticle==key && is_click_acticle?'NvfK4':''">
                      <li class="_2po2r cRfUr" title="" @click="pub_article(true)"><span class=""><i class="fa fa-share _22XWG"></i>直接发布</span></li>
                      <li class="_2po2r cRfUr" title=""><span class=""><i class="fa fa-clock-o _22XWG"></i>定时发布</span></li>
                      <li class="_2po2r cRfUr" title=""><span class="_20tIi"><i class="iconfont ic-paid _22XWG"></i>发布为付费文章</span></li>
                      <li class="_2po2r cRfUr" title=""><span class=""><i class="iconfont ic-set _22XWG"></i>设置发布样式</span></li>
                      <li class="_3nZXj _2_WAp _3df2u _2po2r cRfUr" title="" @mouseout="show_collecion_list=false" @mouseover="show_collecion_list=true">
                        <span class=""><i class="fa fa-folder-open _22XWG"></i>移动文章
                        <div class="_3x4X_">
                          <ul class="_2KzJx oGKRI _2w9pn" :class="!show_collecion_list?'_3DXDE':''">
                            <li class="_2po2r cRfUr" :title="collection.name" v-for="collection,key in collection_list" v-if="current_collection!==key" @click="change_collection(collection.id)">
                              <span class="">{{collection.name}}</span></li>
                          </ul>
                        </div>
                      </span>
                      </li>
                      <li class="_2po2r cRfUr" title=""><span class=""><i class="fa fa-history _22XWG"></i>历史版本</span></li>
                      <li class="_2po2r cRfUr" title=""><span class=""><i class="fa fa-trash-o _22XWG"></i>删除文章</span></li>
                      <li class="_2po2r cRfUr" title=""><span class=""><i class="fa fa-ban _22XWG"></i>设置禁止转载</span></li>
                    </ul>
                  </span>
                </div>
                <span class="NariC">{{article.title}}</span>
                <span class="hLzJv">{{article.content}}</span>
                <span class="_29C-V">字数:{{article.content.length}}</span>
              </li>
            </ul>
            <div class="_2cVn3" @click="add_article('append')"><i class="fa fa-plus"></i><span>在下方新建文章</span></div>
          </div>
        </div>
      </div>
      <input type="text" class="_24i7u" v-model="article_list[current_acticle].title">
      <div id="editor">
        <mavon-editor
          style="height: 100%"
          v-model="article_list[current_acticle].content"
          :ishljs="true"
          ref=md
          @imgAdd="imgAdd"
          @imgDel="imgDel"
          @save="save_article"
        ></mavon-editor>
      </div>
    </div>
  </div>
</template>
<script>
  import { mavonEditor } from 'mavon-editor'
  import 'mavon-editor/dist/css/index.css'
  import '../../static/css/font-awesome/css/font-awesome.css'
    export default {
        name: "Write",
        data(){
            return {
              editorContent:"", //　文章内容
              img_file:[],
              current_collection:0,     // 当前用户选中文章
              collection_form:false,   // 新增输入框
              show_collecion_list: false, // 是否显示文章菜单中的显示文集列表
              is_click_acticle:false,
              collection_name:'',
              current_acticle:0,
              token: '',
              is_click:false,
              collection_list:[
                {"id":1,'name':'散文'},
                {'id':2,'name':'日记本'},
              ],
              article_list:[
                {'id':1,'title':'2020-01-08', 'content': '车市问斩'},
                {'id':2,'title':'2020-01-08', 'content': '车市问斩'},
              ],
            }
        },
        created(){
          this.get_collection();
          this.get_article_list();
        },
        watch:{
          editorContent(){
              console.log(this.editorContent)
          },
          current_collection(){
            this.get_article_list()
          }
        },
        mounted(){
          document.querySelector("#editor").style.height = document.documentElement.clientHeight-document.querySelector("._24i7u").clientHeight+"px";
        },
        components: {
          mavonEditor
        },
        methods:{
          // 绑定@imgAdd event
          imgAdd(pos, $file){
              // 第一步.将图片上传到服务器.
              var formdata = new FormData();
              formdata.append('link', $file);
              this.img_file[pos] = $file;
              this.$axios.post(`${this.$settings.Host}/article/image/`, formdata,{
                  'Content-Type': 'multipart/form-data'
              }).then((res) => {
                  let _res = res.data;
                  console.log(res.data);
                  // 第二步.将返回的url替换到文本原位置![...](0) -> ![...](url)
                  this.$refs.md.$img2Url(pos, _res.link);
              })
          },
          imgDel(pos) {
              delete this.img_file[pos];
          },
          add_article(type){
            // 添加文章
            let date_obj = new Date();
            let month = date_obj.getMonth()+1;
            month = month<10?'0'+month:month;
            let date = date_obj.getDate();
            date = date<10?"0"+date:date;
            let article = {
              "title":`${date_obj.getFullYear()}-${month}-${date}`,
              "content": "",
            };
            let key = 0
            if(type==='insert'){
              // 在文章列表前面添加文章
              this.article_list.splice(0,0,article);
            }else{
              // 在文章列表后面添加文章
              this.article_list.push(article);
              key = this.article_list.length + 1
            }
            // 添加文章到服务器
            console.log(key);
            this.$axios.post(`${this.$settings.Host}/article/`, {
              collection: this.collection_list[this.current_collection].id,
              title: this.article_list[key].title,
              content: this.article_list[key].content,
            },{
              headers:{
                Authorization: 'jwt ' + this.token,
              }
            }).then(response=>{
              this.$message.success('添加文章成功')
            }).catch(error=>{
              this.$message.error('添加文章失败')
            })
          },
          save_article(){
            let article = this.article_list[this.current_acticle]
            // 保存编辑内容
            this.$axios.put(`${this.$settings.Host}/article/${article.id}/save_article/`,{
              'title': article.title,
              'content': article.content,
              'save_id': article.save_id,
              'collection_id': this.current_collection
            },{
              headers:{
                Authorization:'jwt '+this.token,
              }
            }).then(response=>{
              article.save_id = response.data.save_id
            }).catch(error=>{
              this.$message.error('文章内容保存失败！请备份您的内容并及时联系客服工作人员！')
            })
          },
          get_article_list(){
            // 获取当前用户选中文集的文章列表
            let collection = this.collection_list[this.current_collection]
            this.$axios.get(`${this.$settings.Host}/article/`, {
              params:{
                collection:collection.id
              },
              headers:{
                Authorization: "jwt "+this.token
              }
            }).then(response=>{
              this.article_list = response.data;
            }).catch(error=>{
              this.$message.error('对不起，获取文章列表失败')
            })
          },
          get_collection(){
            //  获取用户的文集列表
            let login_token = this.is_login();
            this.$axios.get(`${this.$settings.Host}/article/collection/`, {
              headers:{
                Authorization: 'jwt ' + this.token,
              }
            }).then(response=>{
              this.collection_list=response.data;
            }).catch(error=>{
              this.$message.error('获取文集失败');
            });
          },
          add_collection(){
            // 添加文集
            if(this.collection_name.length<1){
              this.$message.error('文集名不能为空');
            }
            this.is_login();
            this.$axios.post(`${this.$settings.Host}/article/collection/`,{
              name: this.collection_name,
            },{
              headers:{
                Authorization: "jwt " + this.token,
              }
            }).then(response=>{
              this.collection_form = false;
              this.$message.success('添加文集成功！');
            }).catch(error=>{
              this.$message.error('添加文集失败');
              this.article_list.splice(key,1);
            })
          },
          edit_collection(collection){
            this.$confirm(`<input type="text" value="${collection.name}" id="collection_box">`, '请输入新的文集名称', {
              dangerouslyUseHTMLString:true,
              confirmButtonText: '保存',
              cancelButtonText: '放弃修改',
            }).then(()=>{
              let collection_id = collection.id;
              let new_collection = document.querySelector('#collection_box').value;
              collection.name = new_collection;
              // 提交数据到服务器同步
              this.$axios.put(`${this.$settings.Host}/article/collection/${collection_id}/+`,{
                name: collection.name,
              },{
                headers:{
                  Authorization: 'jwt ' + this.token,
                }
              }).then(response=>{

              }).catch(error=>{
                this.$message.error('修改文集失败！当前名称同名或者您没有进行任何修改！')
              });

            }).catch(()=>{

            });
          },
          change_collection(collection_id){
            // 切换文章的文集ID
            let article = this.article_list[this.current_acticle];
            this.$axios.patch(`${this.$settings.Host}/article/${article.id}/change_collection/`,{
              collection_id,
            },{
              headers:{
                Authorization:"jwt "+this.token
              }
            }).then(response=>{
              this.article_list.splice(this.current_acticle,1);
              if(this.article_list.length<1){
                this.add_article();
              }
            }).catch(error=>{
              this.$message.error('切换当前文章的文集失败')
            })
          },
          is_login(){
            let self = this;
            this.token = this.$settings.get_login_user();
            console.log(this.token);
            if(!this.token){
                this.$alert("对不起，请登录后再继续操作！", '警告', {
                  callback(){
                    self.$router.push("/login/");
                  }
                });
                return false;
            }
          },
          pub_article(is_pub){
            console.log(is_pub);
            let article = this.article_list[this.current_acticle];
            this.$axios.patch(`${this.$settings.Host}/article/${article.id}/pub_article/`, {
              is_pub,
            },{
              headers:{
                Authorization:'jwt '+this.token
              }
            }).then(response=>{
              this.$message.success('成功发布文章！');
              setTimeout(()=>{
                this.$router.push(`/${article.id}/writed`)
              },2000);

            }).catch(error=>{
              this.$message.error('发布文章失败！');
            });
          }
        }
    }
</script>

<style scoped>
  body *{
    box-sizing: border-box;
  }
  .write{
    position: absolute;
    top: 0;
    right: 0;
    left: 0;
    bottom: 0;
    margin: 0;
  }
  ._2v5v5 {
    position: relative;
    height: 100%;
    overflow-y: auto;
    background-color: #404040;
    color: #f2f2f2;
    z-index: 100;
    width: 16.66666667%;
    display: block;
    flex: 0 0 auto;
    float: left;
    padding-right: 0;
    padding-left: 0;
    min-height: 1px;
  }
  ._3zibT {
    padding: 30px 18px 5px;
    text-align: center;
    font-size: 14px;
  }
  ._3zibT a {
    display: block;
    font-size: 15px;
    padding: 9px 0;
    color: #ec7259;
    border: 1px solid rgba(236,114,89,.8);
    border-radius: 20px;
    -webkit-transition: border-color .2s ease-in;
    -o-transition: border-color .2s ease-in;
    transition: border-color .2s ease-in;
  }
  ._1iZMb {
    padding: 0 15px;
    margin-top: 20px;
    margin-bottom: 10px;
    font-size: 14px;
    line-height: 1.5;
  }
  ._1iZMb ._33Zlg {
    cursor: pointer;
    color: #f2f2f2;
    transition: color .2s cubic-bezier(.645,.045,.355,1);
    font-size: 14px;
  }
  ._1iZMb ._33Zlg .fa+span {
    margin-left: 4px;
  }
  ._1iZMb ._2G97m {
    overflow: hidden;
  }
  ._1iZMb ._2a1Rp {
    height: 85px;
    opacity: 1;
    margin-top: 10px;
    transition: all .2s ease-out;
    overflow: hidden;
  }
  ._1CtV4 {
    width: 100%;
    height: 35px;
    color: #ccc;
    background-color: #595959;
    border: 1px solid #333;
    padding: 4px 6px;
    font-size: 14px;
    line-height: 20px;
    outline: 0;
    overflow: visible;
    margin: 10px 0 0;
    margin-bottom: 10px;
  }
._3zXcJ {
    position: relative;
    display: inline-block;
    text-align: center;
    height: 30px;
    line-height: 20px;
    padding: 4px 12px;
    border: 1px solid transparent;
    border-radius: 15px;
    font-size: 14px;
    font-weight: 500;
    -ms-touch-action: manipulation;
    touch-action: manipulation;
    cursor: pointer;
    background-image: none;
    white-space: nowrap;
    user-select: none;
    transition: all .2s cubic-bezier(.645,.045,.355,1);
    text-transform: none;
    color: #42c02e;
    border-color: #42c02e;
    margin-left: 4px;
    background-color: #404040;
  }
  .vIzwB {
    color: #999;
    outline: 0;
  }
  ._1iZMb ._1mU5v {
    height: 0;
    opacity: 0;
    margin-top: 0;
  }
  ._1iZMb ._2a1Rp {
    height: 85px;
    opacity: 1;
    margin-top: 10px;
  }
  ._1iZMb ._1mU5v, ._1iZMb ._2a1Rp {
    transition: all .2s ease-out;
  }
  .vIzwB, .vIzwB:focus, .vIzwB:hover {
    background-color: #404040;
    border-color: transparent;
  }
  .dwU8Q {
      margin-left: 4px;
      background-color: #404040;
  }
._3t059 {
    position: relative;
    z-index: 0;
    background-color: #8c8c8c;
}
._3MbJ4 {
    margin-bottom: 0;
}
._3DM7w {
    position: relative;
    line-height: 40px;
    list-style: none;
    font-size: 15px;
    color: #f2f2f2;
    background-color: #404040;
    padding: 0 15px;
    cursor: pointer;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
}
._31PCv {
    background-color: #666;
    border-left: 3px solid #ec7259;
    padding-left: 12px;

}
._3DM7w ._2VLy- {
    float: right;
}
._3P4JX {
    font-size: 16px;
    width: 40px;
    text-align: center;
    position: relative;
    min-height: 30px;
    max-height: 50px;
}
._3DM7w span {
    display: block;
    margin-right: 20px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
._2w9pn {
    font-size: 14px;
    -webkit-box-shadow: 0 5px 10px rgba(0,0,0,.2);
    box-shadow: 0 5px 10px rgba(0,0,0,.2);
    list-style: none;
    background-color: #fff;
    color: #595959;
    border-radius: 6px;
}

._3P4JX ul._2V8zt {
    display: none;
    position: absolute;
    z-index: 99;
    right: 0;
}
._2_WAp ._2KzJx, ._2_WAp ._3x4X_ {
    position: absolute;
    right: 100%;
    top: 0;
}
._2_WAp ._3DXDE {
    display: none;
}
._3P4JX ul._3FcHm {
    top: 100%;
}
._2po2r {
    padding: 10px 20px;
    line-height: 20px;
    white-space: nowrap;
    text-align: left;
    position: relative;
    border-bottom: 1px solid #d9d9d9;
}
._3DM7w:hover, .JUBSP {
    background-color: #666;
}
.h-5Am {
    display: block;
    width: 16.66666667%;
    position: fixed;
    bottom: 0;
    height: 50px;
    line-height: 50px;
    font-size: 15px;
    padding-left: 15px;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    z-index: 150;
    background-color: #404040;
}
.cRfUr {
    border-bottom: 1px solid #d9d9d9;
}
._2po2r:last-child {
    border-radius: 0 0 4px 4px;
    border-bottom: 0;
}
._2po2r:first-child {
    border-radius: 4px 4px 0 0;
}
._2po2r ._22XWG {
    margin-right: 5px;
}
._2po2r:hover {
    background-color: #666;
    color: #fff;
}
._3DM7w span {
    display: block;
    margin-right: 20px;
    overflow: hidden;
    -o-text-overflow: ellipsis;
    text-overflow: ellipsis;
    white-space: nowrap;
}
._3P4JX ul.NvfK4 {
    display: block;
}
._3P4JX ul._2V8zt:before {
    position: absolute;
    right: 12px;
    content: "";
    display: inline-block;
}
._3P4JX ul._3FcHm:before {
    border-left: 9px solid transparent;
    border-right: 9px solid transparent;
    border-bottom: 9px solid #fff;
    top: -9px;
}
.h-5Am .ant-dropdown-trigger {
    display: inline-block;
    color: #999;
    cursor: pointer;
    -webkit-transition: color .2s cubic-bezier(.645,.045,.355,1);
    -o-transition: color .2s cubic-bezier(.645,.045,.355,1);
    transition: color .2s cubic-bezier(.645,.045,.355,1);
}
.h-5Am .fa+span {
    margin-left: 4px;
}
.h-5Am .Yv5Zx {
    float: right;
    margin-right: 15px;
    color: #999;
    cursor: pointer;
  }
  .h-5Am .Yv5Zx i {
      margin-left: 5px;
  }
  .rQQG7{
    height: 100%;
    display: block;
    width: 33.33333%;
    border-right: 1px solid #d9d9d9;
  }
  ._3revO {
    overflow-y: scroll;
    height: 100%;
    position: relative;
  }
  ._3br9T {
    position: relative;
    transition: opacity .3s cubic-bezier(.645,.045,.355,1);
    opacity: 1;
  }
  ._1GsW5 {
    line-height: 20px;
    font-size: 15px;
    font-weight: 400;
    padding: 20px 0 20px 25px;
    cursor: pointer;
    color: #595959;
  }
  ._1GsW5:hover {
    color: #262626;
  }
  ._2TxA- {
    position: relative;
    margin-bottom: 0;
    background-color: #efe9d9;
    border-top: 1px solid #d9d9d9;
  }
  ._25Ilv {
    position: relative;
    height: 90px;
    color: #595959;
    background-color: #fff;
    margin-bottom: 0;
    padding: 15px 10px 15px 60px;
    box-shadow: 0 0 0 1px #d9d9d9;
    border-left: 5px solid transparent;
    list-style: none;
    line-height: 60px;
    cursor: pointer;
    user-select: none;
  }
  ._25Ilv ._2m93u {
    background: url(/static/image/sprite.9d24217.png) no-repeat -50px -25px;
    background-size: 250px;
    position: absolute;
    top: 30px;
    left: 20px;
    width: 22px;
    height: 30px;
  }
  ._1tqbw, ._25Ilv:hover, ._33nt7 {
    background-color: #e6e6e6;
  }
  ._25Ilv ._2m93u {
    background: url(/static/image/sprite.9d24217.png) no-repeat -50px -25px;
    background-size: 250px;
    position: absolute;
    top: 30px;
    left: 20px;
    width: 22px;
    height: 30px;
  }
  ._3P4JX {
    font-size: 16px;
    width: 40px;
    text-align: center;
    position: relative;
    min-height: 30px;
    max-height: 50px;
}
  ._25Ilv .poOXI {
    float: right;
}
  ._33nt7 {
    border-left-color: #ec7259;
  }
  ._25Ilv .hLzJv, ._25Ilv .NariC {
    display: block;
    height: 30px;
    line-height: 30px;
    margin-right: 40px;
    overflow: hidden;
    -o-text-overflow: ellipsis;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-size: 18px;
    font-family: sans-serif;
}
  ._2TxA- {
    position: relative;
    margin-bottom: 0;
    background-color: #efe9d9;
    border-top: 1px solid #d9d9d9;
}
  ._3P4JX ul._2V8zt {
    display: none;
    position: absolute;
    z-index: 99;
    right: 0;
}
  ._3P4JX ul._3FcHm {
    top: 100%;
}
  ._2w9pn {
    font-size: 14px;
    box-shadow: 0 5px 10px rgba(0,0,0,.2);
    list-style: none;
    background-color: #fff;
    color: #595959;
    border-radius: 6px;
}
  ._3P4JX ul.NvfK4 {
    display: block;
}
  ._3P4JX ul._3FcHm:before {
    border-left: 9px solid transparent;
    border-right: 9px solid transparent;
    border-bottom: 9px solid #fff;
    top: -9px;
}
  ._3P4JX ul._2V8zt:before {
    position: absolute;
    right: 12px;
    content: "";
    display: inline-block;
}
._25Ilv ._13kgp {
    position: absolute;
    top: 30px;
    left: 20px;
    width: 22px;
    height: 30px;
    background: url(/static/image/sprite.9d24217.png) no-repeat 0 -25px;
    background-size: 250px;
}
._25Ilv ._13kgp {
    position: absolute;
    top: 30px;
    left: 20px;
    width: 22px;
    height: 30px;
    background: url(/static/image/sprite.9d24217.png) no-repeat 0 -25px;
    background-size: 250px;
}
._25Ilv ._2m93u {
    background: url(/static/image/sprite.9d24217.png) no-repeat -50px -25px;
    background-size: 250px;
}
._25Ilv ._29C-V {
    position: absolute;
    bottom: 2px;
    left: 5px;
    font-size: 9px;
    line-height: 16px;
    color: #595959;
}
._2cVn3 {
    line-height: 30px;
    padding: 20px 0 20px 25px;
    cursor: pointer;
    color: #999;
    margin-bottom: 80px;
}
._24i7u {
    flex-shrink: 0;
    padding: 0 80px 10px 40px;
    margin-bottom: 0;
    border: none;
    font-size: 30px;
    font-weight: 400;
    line-height: 30px;
    box-shadow: none;
    color: #595959;
    background-color: transparent;
    outline: none;
    border-radius: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    position: absolute;
    top: 0;
    right: 0;
    width: 66.666666%;
}
  #editor {
    margin: auto;
    width: 66.666666%;
    position: absolute;
    right: 0;
    top: 44px;
    height: 580px;
  }
</style>
