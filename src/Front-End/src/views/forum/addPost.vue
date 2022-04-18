<template>
  <body style="margin-top:1%;		border: 1px solid #ddd;">
  <h1>New Post</h1>
  <el-form ref="form" :model="form" label-width="80px" :rules="rules">
    <el-form-item label="title" prop="title">
      <el-input v-model="form.title" ></el-input>
    </el-form-item>
    <!--进行列表渲染，数据全部存在Vuex的全局静态变量里，修改分区数只需要修改store/index.js的静态数据-->
    <el-form-item label="tag" prop="category">
      <el-select  filterable v-model="form.category" placeholder="choose tag">
        <el-option
          v-for="item in tagsList"
          :key="item"
          :value="item"
          :label="item"
        >
        </el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="content" prop="content">
      <el-input type="textarea" v-model="form.content" :rows="20"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="onSubmit">Post</el-button>
      <el-button>
        <router-link :to="{ name: 'forum/All'}">
            cancel
		</router-link>
      </el-button>
    </el-form-item>
  </el-form>

  </body>

</template>

<script>
import { createPost } from '@/api/forum'
import axios from "axios";

export default {
  data() {
    return {
      postsId:'',
      tagsList:['Discussion','Recruit','Help'],
      form: {
        title: '',
        category: '',
        content: ''
      },
      rules:{
        title:[{required : true,message: 'please enter title',trigger:'blur'}],
        content:[{required : true,message: 'please enter content',trigger:'blur'}],
        category:[{required : true,message: 'please choose tag',trigger:'change'}],
      }
    }
  },
  methods: {
    onSubmit() {
      //alert('submit!');
      if(this.form.content===''||this.form.title===''||this.form.category==="")
      {
        alert("Post it by filling in all required fields")
      }
      else {
        var form={
        postTitle:this.form.title,
        content:this.form.content,
        tag:this.form.category,
        userID:this.$store.state.user.token
        }
          // alert('succss')
          createPost(form).then(res => {
            if (res.data['success']){
              this.$message({
                message: 'Register Successfully',
                type: 'success'
              })
              this.$router.push("/forum/all")
            } else{
              this.$alert("Create post fail!")
            }
        })
        .catch(function (error) { // 请求失败处理
        console.log(error);
      })
      }
    }
  }
}
</script>

<style scoped>
	body {
		background-color: white;
		padding: 0.5rem;
		margin: 4rem 3rem;
	}
</style>
