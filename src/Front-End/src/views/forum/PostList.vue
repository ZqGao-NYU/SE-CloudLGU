<template>
<div style="width:80%;margin-left:10%;margin-top:3%;">
	<div>
			<div v-for="tag in tagsList" :key="tag">
				<div class="tag">
					<el-button @click="clickroute(tag)">
						{{tag}}
					</el-button>
				</div>
			</div>
			<div class="tag">
				<router-link :to="{name:'add_post'}">
					<el-button type="info">
						Post Now
					</el-button>
				</router-link>
			</div>
			</div>
	<div class="PostList">
	    <div class="loading" v-if="loading">
	        Loading...
	    </div>
	    <div class="posts" v-else>

			<ul>
				<li v-for="post in posts" :key="post.postID">
					<span style="font-weight: 900; color: #ff0000;float: left;margin-left:-3%">
						<div v-if="post.tag == 'Top'">TOP</div>
					</span>
					<span style="font-size:1.2rem; font-weight: 600; float:left;margin-left:2%;">
						<div style="width:10px;">{{post.poster}} </div>
					</span>
					<span style="margin-left:80px;">
					<router-link :to="{ name: 'post_content', params: {postID: post.postID}}" :title="post.title">
						{{ post.title }}
					</router-link>
					</span>
					<div style="font-size:0.8rem ;color:#a8a3a3 ;float: right; margin-right:2%">
						{{ post.updateTime.substring(0,10)}}  {{ post.updateTime.substring(11,16)}} 
					</div>
				</li>
			</ul>
	    </div>
	</div>
</div>
</template>

<script>
import { showAllPost } from '@/api/forum'

	export default {
	  data () {
	    return {
		  source:{
			  success: true,
			  postList:[
				{
					title: '第一个post',
					content: '第一个post的内容',
					tag: 'Discussion',
					poster: 'poster1',
					createTime: '2021-02-01T12:22:12',
					updateTime: '2021-02-01T12:22:12'
				},
				{
					title: '第2个post',
					content: '第2个post的内容',
					tag: 'Top',
					poster: 'poster2',
					createTime: '2021-02-01T12:22:12',
					updateTime: '2021-02-01T12:22:12'
				},
				{
					title: '第3个postlongtitleeeeeeeeeeeeeeeeeeeeeeeeee',
					content: '第2个post的内容',
					tag: 'Help',
					poster: 'posr6',
					createTime: '2021-02-01T12:22:12',
					updateTime: '2021-02-01T12:22:12'
				}
			  ]
		  },
		  webTag: 'All',
		// post: {title: '',
		// content: '',
		// tag: '',
		// poster: '',
		// createTime: '',
		// updateTime: ''},
		  posts:[],
	      loading:false,
		  tagsList:['All','Discussion','Recruit','Help']
	    }
	  },
		// watch: {
		// 	$route: {
		// 	immediate: true, // 一旦监听到路由的变化立即执行
		// 	handler(to, from) {
		// 		alert("监听路由：" + JSON.stringify(to.name))
		// 		// this.webTag = this.$route.params.webTag;
		// 		alert(this.webTag)
		// 	}
		// 	}
		// },
	  created () {
	showAllPost()
    .then(res => {
      if (res.data['success']){
		this.posts=[{
		title: '',
		content: '',
		tag: 'Top',
		poster: '',
		postID: 0,
		createTime: '',
		updateTime: ''
	}]
	console.log(res.data)
			for (var i = 0; i < res.data['postList'].length; i++) {
				if (res.data['postList'][i]['postTag'] == 'Top') {
					this.posts[0] = {
					postID:res.data['postList'][i]['postID'],
						title:res.data['postList'][i]['postTitle'],
						content: res.data['postList'][i]['postContent'],
						tag: res.data['postList'][i]['postTag'],
						poster: res.data['postList'][i]['posterName'],
						createTime: res.data['postList'][i]['createTime'],
						updateTime: res.data['postList'][i]['updateTime']
					}
				} else if (res.data['postList'][i]['postTag'] == this.webTag || this.webTag == 'All') {
				this.posts.push({
									postID:res.data['postList'][i]['postID'],

					title:res.data['postList'][i]['postTitle'],
						content: res.data['postList'][i]['postContent'],
						tag: res.data['postList'][i]['postTag'],
						poster: res.data['postList'][i]['posterName'],
						createTime: res.data['postList'][i]['createTime'],
						updateTime: res.data['postList'][i]['updateTime']
				})
				}
			}
      } else{
        this.$alert("Create post fail!")
      }
    })
    .catch(function (error) { // 请求失败处理
      console.log(error);
    })
	  },
	  methods: {
		  clickroute: function (Tag) {
		  showAllPost()
    .then(res => {
      if (res.data['success']){
		this.posts=[{
		title: '',
		content: '',
		tag: 'Top',
		poster: '',
		postID: 0,
		createTime: '',
		updateTime: ''
	}]
	console.log(res.data)
			for (var i = 0; i < res.data['postList'].length; i++) {
				if (res.data['postList'][i]['postTag'] == 'Top') {
					this.posts[0] = {
					postID:res.data['postList'][i]['postID'],
						title:res.data['postList'][i]['postTitle'],
						content: res.data['postList'][i]['postContent'],
						tag: res.data['postList'][i]['postTag'],
						poster: res.data['postList'][i]['posterName'],
						createTime: res.data['postList'][i]['createTime'],
						updateTime: res.data['postList'][i]['updateTime']
					}
				} else if (res.data['postList'][i]['postTag'] == Tag || Tag == 'All') {
				this.posts.push({
									postID:res.data['postList'][i]['postID'],

					title:res.data['postList'][i]['postTitle'],
						content: res.data['postList'][i]['postContent'],
						tag: res.data['postList'][i]['postTag'],
						poster: res.data['postList'][i]['posterName'],
						createTime: res.data['postList'][i]['createTime'],
						updateTime: res.data['postList'][i]['updateTime']
				})
				}
			}
      } else{
        this.$alert("Create post fail!")
      }
    })
    .catch(function (error) { // 请求失败处理
      console.log(error);
    })
		  },

	  }
	}
</script>

<style scoped>
	.tag {
		float:left;
		text-align: center;
		background:#ffffff ;
		height: 50px;
		width: 20%;
		/* margin-top: 50px; */
		/* margin-left: 200px; */
	}
	.el-button {
		color: #000000;
		font-size: 1.5rem;
		border: 1px solid #dcdfe6;
		width: 100%;
		text-align: center;
		/* vertical-align:middle; */
		height: 50px;
		padding-bottom:0%;
	}
	.PostList {
		background-color: #ffffff;
	}
	.PostList .posts li {
	list-style: none;
	/* margin-top: 30px; */
	margin-bottom: 14px;
	border-bottom: 1px solid #E7E7E7;
	line-height: 80px;
	}

	.router-link-active {
	text-decoration: none;
	color: purple;
	}
	a{
	text-decoration: none;
	color: black;
	}


</style>
