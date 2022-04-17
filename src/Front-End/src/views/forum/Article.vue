<template>
	<div class="ArticleSection">
	    <div class="loading" v-if="loading">
	        Loading...
	    </div>
	    <div class="article" v-else>
			<div style="float:left;width:100%;margin-left:-2.5%;margin-top:-2%;margin-bottom:2%">
				<router-link :to="{ name: 'forum/All'}">
					<el-button size='mini'>Back</el-button>
				</router-link>
			</div>
			<h1>{{this.postTitle}}</h1>
			<ul>
				<li>• 分类: {{ this.postTag }}</li>
				<li>• 发布于: {{ this.createTime }}</li>
				<li>• 作者: {{ this.posterName }}</li>
			</ul>
			<div id="content"> {{this.postContent}}</div>
		<el-button style="margin-left:87%; margin-bottom: 10px" @click="docomment()"> Comment</el-button>
		</div>
        <div id='reply'>
			<div v-if="commenting"> 
			<div class='replySec'>
				<el-input v-model="message" placeholder="comment" clearable> </el-input>
				<el-form style="margin-left: 77%; margin-top: 10px">
				<el-button @click="sendComment()"> comment</el-button>
				<el-button @click="docomment()"> cancel</el-button>
				</el-form>
			</div>
		</div>

            <div v-for='(comment, index) in this.commentList' class='replySec' :key="comment.commentID">
                <div >
					<span style="font-size:1.2rem;font-weight: 600;">{{comment.userID}}</span>
       			    <span style="font-size:0.8rem;color:#a8a3a3 ;">
       			    	{{index + 1}}楼
       			    </span>
                </div>
                <p>{{comment.commentContent}}</p>
				<div v-if="comment.userID==userID">
				<el-button type="text" style="float:right; font-size:0.8rem;margin-top:-5%;" @click="deleteComment(comment.commentID)"> Detele</el-button>
				</div>
            </div>
    	</div>
	</div>
</template>

<script>
	export default {
		name: 'Article',
	    data () {
		    return {
			  message: '',
			  userID: 122,
			  source:{
				    success: true,
					postTitle: 'Title of the post (String)',
					postContent: 'Content of the post (String)',
					postTag: 'study',
					posterName: 'Name of the poster(String)',
					createTime: '2022-02-02T11:12:12',
					updateTime: '2022-02-02T11:12:12',
					commentList: [{
						commentID: 999,
						userID: 1676,
						commentContent:'commentttttt'
					},{
						commentID: 199,
						userID: 1676,
						commentContent:'commentttttt'
					}]
			  },
		      postID: 0,
			  postTitle: 'hh',
			  postContent: '',
			  postTag: '',
			  posterName: '',
			  createTime: '',
			  updateTime: '',
			  commentList: [],
	  	      loading:false,
			  commenting: false
		    }
		},
		created () {
			// postID = this.$router.params.postID
			this.postTitle = this.source.postTitle
			this.postContent = this.source.postContent
			this.postTag = this.source.postTag
			this.posterName = this.source.posterName
			this.createTime = this.source.createTime
			this.updateTime = this.source.updateTime
			this.commentList = this.source.commentList
			// loading: true
		},
	  	methods: {
			docomment: function () {
				this.commenting = !this.commenting
				this.message=''
			},
			sendComment: function () {
				this.commentList.push ({
					commentID: 9,
					userID: this.userID,
					commentContent:this.message
				})
				this.message=''
				this.commenting = false
			},
			deleteComment: function (id) {
				let index = this.commentList.findIndex(e => e.commentID === id)
          		this.commentList.splice(index, 1)
			}
		  	// getData(){
		  	// 	//获取文章信息
			// 	this.$http({
		    //         url: `https://cnodejs.org/api/v1/topic/${this.$route.params.id}`,   //ES6语法，引入组件内的 route object（路由信息对象） 
		    //         method: 'get',
		    //         params:{
		    //         	mdrender:true
		    //         }
		    //       })
			// 	  .then( (response) => {
			// 	  	if( response.data.success === true ){
			// 	  		this.post = response.data.data;
			// 	  		this.loading = false;
			// 	  	}
			// 	  })
			// 	  .catch(function (error) {
			// 	  	console.log(error);
			// 	  });
		  	// }
		// },
	    // beforeMount() {
	    // 	this.loading = true;
	    //     this.getData();
	    // },
	    // watch:{
		// 	$route(){
		// 		this.getData();
		// 	}
		}
	}
</script>

<style>
	/* @import url("../assets/markdown-github.css"); */
	.ArticleSection {
		-webkit-box-sizing: border-box;
		-moz-box-sizing: border-box;
		box-sizing: border-box;
		display: inline-block;
		width: 80%;
		border: 1px solid #ddd;	
	    padding: 0.8rem 0.4rem;
	    margin-left: 5%;
		margin-top:3%;
	}
	.floor {
		/* display: inline-block; */
		/* /* font-size:0.8rem ; */
		color:#a8a3a3;
		/* padding-left: 5px;  */
	}
	.ArticleSection #content {
		padding: 2rem 1rem 2rem 1rem;
		line-height: 1.6;
		padding-bottom: 1rem;
	}
	.ArticleSection > h1 {
		font-size: 0.1rem;
	}
	.article {
		background: white;
   	    margin-bottom: 10px;
        padding-left: 20px;
        padding-top: 10px;
		border-bottom: 1px solid #C0CCDA;

	}
	.article h1 {
		font-size:1.2rem;
		font-weight: 600;
	}
	.article >ul li {
		display: inline-block;
		font-size:0.8rem ;
		color:#a8a3a3 ;
		padding-left: 5px;
	}
	.article li a {
	    color: inherit;
   		 text-decoration: none;
	}
    .replySec {
        box-sizing: border-box;
        border-bottom: 1px solid #C0CCDA;
        width: 100%;
        padding: 1rem;
        background: white;
    }
    #reply {
        display: flex;
        flex-direction: column;
    }
    .replyUp {
    	display: inline-block;
    }
    .replyUp span {
    	display: inline-block;
	    vertical-align: top;
	    margin-top: 7px;
	    margin-left: 6px;
	    font-size: 14px;
	    color: #806767;
    }
    .thumbsClass {
    	float: right;
    }
    .replyUp > a{
    	color: black;
	   	text-decoration: none;
		font-weight: 600;
    }
    .replyUp a:nth-of-type(2) {
    	margin-left: -14px;
    	vertical-align: super;
    }
    .thumbsClass  {
    	color: red;
    }
    .replySec > p {
    	padding-left: 50px;
    	clear: both;
    }
	.soller{
		position: fixed;
		top: 50%;
		border: 1px solid rgba(0,0,0,0);
	}
	.soller ul{
		margin-top: -200px;
	}
	.soller ul li{
		width: 80px;
		height: 80px;
		margin: 10px 0 0;
		list-style: none;
		text-align: center;
	}
</style>