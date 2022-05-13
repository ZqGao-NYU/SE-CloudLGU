<template>
  <div class="personalCenter">
    <el-container>
      <el-header> Basic Information </el-header>
      <el-container style="height:650px">
        <el-aside width="400px">
          <el-col :span="12">
            <div class="sub-title" />
            <div class="demo-basic--circle">
              <div class="img">
                <el-avatar
                  id="imgage"
                  :size="100"
                  :src="valueUrl"
                  align="center"
                />
              </div>
              <div class="block">
                <span> {{ name }} </span>
              </div>
            </div>
          </el-col>

          <el-button-group style="float: right; padding: 3px 0" type="text">
            <v-btn color="#50A75E" class="submit white--text" height="30" style="margin-left:20px;" @click="$refs.inputFile.click()">Upload Avatar</v-btn>
            <input v-show="false" ref="inputFile" type="file" accept="image/*" @change="uploadFile($event)">
          </el-button-group>
        </el-aside>
        <el-container>
          <el-main>
            <el-card class="box-card">
              <div>
                <span style="float: left" shadow="hover"><b>Name</b></span>
                <br>
                <span> {{ name }} </span>
                <el-divider />
                <span style="float: left" shadow="hover"><b>Email</b></span>
                <br>
                <span> {{ email }} </span>
                <el-divider />
                <span style="float: left" shadow="hover"><b>Self Introduction</b></span>
                <br>
                <span> {{ intro }} </span>
                <el-divider />
                <span style="float: left" shadow="hover"><b>Identity</b></span>
                <br>
                <span> {{ identity }} </span>
                <el-divider />
              </div>
              <v-btn color="#64d978" class="submit white--text" height="30" @click="toggleModify">Modify</v-btn>
              <v-btn color="#64d9d6" class="submit white--text" height="30" style="margin-left:20px;" @click="goChangePassword">Change Password</v-btn>
            </el-card>
          </el-main>
        </el-container>
      </el-container>
    </el-container>
    <div class="edit_dialog">
      <el-dialog
        title="Edit User Information"
        :visible.sync="editdialogVisible"
        width="50%"
        style="font-family: Lucida Sans; color:#000000"
        append-to-body
      >
        <el-form ref="edit_user" label-width="100px" :model="edit_user" :rules="edit_rules">
          <el-form-item label="Username" prop="username">
            <el-input v-model="edit_user.username" placeholder="" />
          </el-form-item>

          <el-form-item label="Intro" prop="intro">
            <el-input v-model="edit_user.intro" placeholder="" />
          </el-form-item>
          <el-form-item el-form-item>
            <v-btn color="#FBE87985" class="cancel#AAAAAA--text" height="30" @click="cancelEdit">Cancel</v-btn>
            <v-btn color="#50A75E" class="submit white--text" height="30" style="margin-left:20px;" @click="handleUpdate">Submit</v-btn>
          </el-form-item>
        </el-form>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import { updateProfile, updateAvatar } from '@/api/personalCenter'
export default {
  //user profile page
  name: 'BasicInformation',
  data() {
    return {
      valueUrl: '',
      name: '',
      email: '',
      intro: '',
      identity: '',
      editdialogVisible: false,
      edit_user: {
        username: '',
        intro: ''
      },
      edit_rules: {
        username: [{
          min: 5,
          max: 12,
          message: 'Range within 5 to 12 characters',
          trigger: 'blur'
        }],
        intro: [{
          min: 0,
          max: 40,
          message: 'maximum 40 characters',
          trigger: 'blur'
        }]
      }
    }
  },
  created() {
    // get user profile in Cookies
    this.valueUrl = this.$store.state.user.avatar
    this.name = this.$store.state.user.name.replace(/\s*/g, '') //no space allowed
    this.email = this.$store.state.user.email
    this.intro = this.$store.state.user.intro
    this.identity = this.$store.state.user.roles[0]
    console.log(this.valueUrl)
  },
  methods: {

    toggleModify() {
      this.edit_user.username = this.name
      this.edit_user.intro = this.intro
      this.editdialogVisible = true
    }, //toggle modify. can only modify name, introduction and avatar
    handleUpdate() {
      // send avatar and name, intro seperately
      updateProfile(this.$store.state.user.token, this.edit_user).then(res => { //call API
        console.log('---basic info: send updated profile successfully')
        if (res.data['success']) {
          this.$message({
            message: 'Update Profile Successfully',
            type: 'success'
          })
          this.editdialogVisible = false
          this.$router.go(0) //refresh page to show the updated profile
        } else {
          this.$message({
            message: 'Update Profile Failed! Please try again',
            type: 'error'
          })
          this.edit_user.name = this.name
          this.edit_user.intro = this.intro
          this.editdialogVisible = false
        } //close the edit dialog
      })
    },
    uploadFile(el) {
      // upload image file
      if (!el.target.files[0].size) return // if file size = 0, return
      if (el.target.files[0].type.indexOf('image') === -1) { // make sure an image is selected
        return
      } else {
        const that = this
        const reader = new FileReader() // read file
        reader.readAsDataURL(el.target.files[0]) // read file
        reader.onload = function() {
          // after reading, get the url
          that.valueUrl = this.result
          // console.log(that.valueUrl);
        }
        // const uid = 'e0c9dd3de0418e698d49984ae035992a'; //uid needed for back-end
        var formData = new FormData() // formdata
        // formData.append('res', el.target.files[0]);
        formData.append('userID', this.$store.state.user.token)
        formData.append('photo', el.target.files[0])
        // post the image to back-end
        updateAvatar(formData).then(res => { //call API
          if (res.data['success']) {
            this.$message({
              message: 'Update Profile Successfully',
              type: 'success'
            })
            this.$router.go(0)
          } else {
            this.$message({
              message: 'Update Profile Failed! Please try again',
              type: 'error'
            })
            this.$router.go(0)
          }
        }) //refresh the page
      }
    },
    cancelEdit() {
      this.edit_user.username = this.name
      this.edit_user.intro = this.intro
      this.editdialogVisible = false
    }, //cancel editing
    goChangePassword() {
      this.$router.push('/personalCenter/changePassword')
    } // go to change password
  }
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
