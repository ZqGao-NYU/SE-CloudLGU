<template>
  <div class="ArticleSection">
    <div v-if="loading" class="loading">
      Loading...
    </div>
    <div v-else class="article">
      <div style="float:left;width:100%;margin-left:-2.5%;margin-top:-2%;margin-bottom:2%">
        <router-link :to="{ name: 'forum/All'}">
          <el-button size="mini">Back</el-button>
        </router-link>
      </div>
      <h1 style="font-size:2rem;">{{ this.postTitle }}</h1>
      <ul>
        <li>• Tag: {{ this.postTag }}</li>
        <li>  • public: {{ this.createTime }}</li>
        <li>  • Auther: {{ this.posterName }}</li>
      </ul>
      <div id="content"> {{ this.postContent }}</div>
      <el-button style="margin-left:87%; margin-bottom: 10px" @click="docomment()"> Comment</el-button>
    </div>
    <div id="reply">
      <div v-if="commenting">
        <div class="replySec">
          <el-input v-model="message" placeholder="comment" clearable />
          <el-form style="margin-left: 77%; margin-top: 10px">
            <el-button @click="sendComment()"> comment</el-button>
            <el-button @click="docomment()"> cancel</el-button>
          </el-form>
        </div>
      </div>

      <div v-for="(comment, index) in this.commentList" :key="comment.commentID" class="replySec">
        <div>
          <span style="font-size:0.9rem;font-weight: 600;">{{ comment.commenterName }}</span>
          <span style="font-size:0.7rem;color:#a8a3a3 ;">
            {{ index + 1 }}
          </span>
        </div>
        <p>{{ comment.commentContent }}</p>
        <div v-if="comment.userID==ID">
          <el-button type="text" style="float:right; font-size:0.8rem;margin-top:-3%;" @click="deletiComment(comment.commentID)"> Detele</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { showPost, createComment, deleteComment } from '@/api/forum'

export default {
  name: 'Article',
	    data() {
		    return {
			  message: '',
			  userID: 122,
		    postID: 0,
        ID: '',
			  postTitle: 'hh',
			  postContent: '',
			  postTag: '',
			  posterName: '',
			  createTime: '',
			  updateTime: '',
			  commentList: [],
	  	      loading: false,
			  commenting: false,
      createTime: ''
		    }
  },
  created() {
    var id = this.$store.state.user.token
    this.ID = id
    console.log(this.$route.params)
    var postID = this.$route.params.postID
    console.log(postID)
    // load and show all post information from api
    showPost(postID)
      .then(res => {
        console.log('here')
        console.log(res.data['commentList'])
        if (res.data['success']) {
          this.postTitle = res.data['postTitle']
          this.postTag = res.data['postTag']
          this.posterName = res.data['posterName']
          this.postContent = res.data['postContent']
          this.createTime = res.data['createTime'].substring(0, 10) + '  ' + res.data['createTime'].substring(11, 16)
          this.updateTime = res.data['updateTime']
          this.commentList = res.data['commentList']
        } else {
          this.$alert('Create post fail!')
        }
      })
      .catch(function(error) { // request failure error
        console.log(error)
      })
  },
	methods: {
    docomment: function() {
      this.commenting = !this.commenting
      this.message = ''
    },
    // send a new comment
    sendComment: function() {
      console.log(this.message)
      var commentForm = { postID: this.$route.params.postID,
        userID: this.$store.state.user.token,
        commentContent: this.message }
      // send request to api to create a comment
      createComment(commentForm)
        .then(res => {
          if (res.data['success']) {
            this.$message({
              message: 'Comment Successfully',
              type: 'success'
            })

            this.message = ''
            this.commenting = false
            this.$router.go(0)
          } else {
            this.$alert('Create post fail!')
          }
        })
        .catch(function(error) { // request failure error
          console.log(error)
        })
    },
    // delete comment
    deletiComment: function(id) {
      // send delete request to api
      deleteComment(id)
        .then(res => {
          console.log(id)
          if (res.data['success']) {
            this.$message({
              message: 'Delete Successfully',
              type: 'success'
            })
            const index = this.commentList.findIndex(e => e.commentID === id)
            this.commentList.splice(index, 1)
          } else {
            this.$alert('Create post fail!')
          }
        })
        .catch(function(error) { // request failure error
          console.log(error)
        })
    }
  }
}
</script>

<style>
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
		color:#a8a3a3;
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
