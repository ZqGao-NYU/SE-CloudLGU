<template>
  <div class="personalCenter">
    <el-container >
      <el-header> Basic Information </el-header>
      <el-container>
        <el-aside width="400px">
          <el-col :span="12">
            <div class="sub-title"></div>
            <div class="demo-basic--circle">
              <div class="img">
                <el-avatar
                  :size="100"
                  :src="valueUrl"
                  align="center"
                ></el-avatar>
              </div>
              <div class="block">
                <span> {{name}} </span>
              </div>
            </div>
          </el-col>
          
          <el-button-group style="float: right; padding: 3px 0" type="text">
            <el-button type="primary" size="medium" round>Upload Avatar</el-button>
            <input @change="uploadFile($event)" type="file" accept="image/*"/>  
          </el-button-group>
        </el-aside>
        <el-container>
          <el-main>            
            <el-card class="box-card">
              <div>
                <span style="float: left" shadow="hover"><b>Name</b></span>
                <br/>
                <el-input v-model="name" class="disInputStyle" :disabled="!change" />
                <el-divider></el-divider>
                <span style="float: left" shadow="hover"><b>Email</b></span>
                <br/>
                <span> {{ email }} </span>
                <el-divider></el-divider>
                <span style="float: left" shadow="hover"><b>Self Introduction</b></span>
                <br/>
                <el-input v-model="intro" class="disInputStyle" :disabled="!change"/>
                <el-divider></el-divider>
                <span style="float: left" shadow="hover"><b>Identity</b></span>
                <br/>
                <span> {{ identity }} </span>
                <el-divider></el-divider>
              </div>
              <el-button type="primary" size="medium" round @click="toggleModify">Modify</el-button>
              <el-button type="primary" size="medium" round @click="handleUpdate">Save</el-button>
            </el-card>
          </el-main>
        </el-container>
      </el-container>
    </el-container>
  </div>
</template>

<script>

export default {
  name: 'BasicInformation',
  data() {
    return {
      valueUrl: '',
      name: '',
      email: '',
      intro: '',
      identity: '',
      change: false
    }
  },
  created(){
    this.valueUrl = this.$store.state.user.avatar
    this.name = this.$store.state.user.name
    this.email = this.$store.state.user.email
    this.intro = this.$store.state.user.intro
    this.identity = this.$store.state.user.roles[0]
  },
  methods: {
    toggleModify(){
      this.change = true
    },
    handleUpdate(){
      this.$alert('update ')
      this.change = false
    },
    uploadFile (el) {
      if (!el.target.files[0].size) return; // if file size = 0, return
      if (el.target.files[0].type.indexOf('image') === -1) { //make sure an image is selected
      return
      } else {
        const that = this;
        const reader = new FileReader(); // read file
        reader.readAsDataURL(el.target.files[0]); // read file
        reader.onload = function () {
          // after reading, get the url
          that.valueUrl = this.result;
          console.log(that.valueUrl);
        };
        const uid = 'e0c9dd3de0418e698d49984ae035992a'; //uid needed for back-end
        const formData = new FormData();  // formdata
        formData.append('res', el.target.files[0]); 
        formData.append('uid', uid);
        //post the image to back-end
        console.log(formData);
        console.log(el.target.files[0]);
        //this.$router.go(0)
      }
    },

  },
}  
</script>


<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}

.disInputStyle{
  text-align: center;
}

.personalCenter {
  min-height: 100%;
  height: 100%;
  background-color: #e9eef3;
}

.user-avatar {
  cursor: pointer;
  width: 40px;
  height: 40px;
  border-radius: 10px;
}

.el-header {
    line-height: 60px;
    text-align: center;
    background-color: #b3c0d1;
  }
  .el-aside {
    line-height: 44px;
    text-align: center;
    background-color: #d3dce6;
  }
  .el-main {
    min-height: 100%;
    line-height: 36px;
    text-align: center;
    background-color: #e9eef3;
  }

  .demo-basic--circle {
    margin-top: 30px;
    margin-left: 150px;
  }
  .block {
    margin-left: 25px;
    font-weight: bold;
  }
  .text {
    font-size: 14px;
  }
  .item {
    margin-bottom: 18px;
  }
  .clearfix:before,
  .clearfix:after {
    display: table;
    content: '';
  }
  .clearfix:after {
    clear: both;
  }

  .box-card {
    margin-left: 10%;
    min-height: 100%;
    
    width: 80%;
    border-radius: 30px;
  }
</style>