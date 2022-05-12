<template>
  <div class="login-container">
    <div v-show="!showEmail" class="login-container">
      <el-form ref="pswForm" :model="pswForm" :rules="pswRules" class="login-form" auto-complete="off" label-position="left">

        <div class="title-container">
          <h1 class="title">Change Password</h1>
        </div>

        <div class="title-input">
          <h3 class="title">Old Password:</h3>
        </div>
        <el-form-item prop="oldPassword">
          <span class="svg-container">
            <svg-icon icon-class="password" />
          </span>
          <el-input
            :key="passwordType"
            ref="oldPassword"
            v-model="pswForm.oldPassword"
            :type="passwordType"
            placeholder="Please enter the old password"
            name="password"
            tabindex="2"
            auto-complete="on"
          />
        </el-form-item>

        <div class="title-input">
          <h3 class="title">New Password:</h3>
        </div>
        <el-form-item prop="password">
          <span class="svg-container">
            <svg-icon icon-class="password" />
          </span>
          <el-input
            :key="passwordType"
            ref="password"
            v-model="pswForm.password"
            :type="passwordType"
            placeholder="Please enter the new password"
            name="password"
            tabindex="2"
            auto-complete="on"
          />
        </el-form-item>

        <div class="title-input">
          <h3 class="title">Repeat Password:</h3>
        </div>
        <el-form-item prop="password2">
          <span class="svg-container">
            <svg-icon icon-class="password" />
          </span>
          <el-input
            :key="passwordType"
            ref="password2"
            v-model="pswForm.password2"
            :type="passwordType"
            placeholder="Please repeat the password"
            name="password2"
            tabindex="2"
            auto-complete="on"
          />
        </el-form-item>

        <el-button :loading="loading" type="primary" style="width:100%;margin-bottom:30px;" @click.native.prevent="handlePasswordReset()">
          Confirm
        </el-button>

        <el-button type="primary" style="width:100%;margin-left:-1px;" @click.native.prevent="cancel()">
          Cancel
        </el-button>

        <div class="tips" style="margin-left: 30px;">
          <span style="margin-right:30px;">Forgot your password?</span>
          <a class="asp" @click="changeMethod()">Use email verification</a>
        </div>
      </el-form>
    </div>

    <div v-show="showEmail" class="login-container">
      <el-form ref="codeForm" :model="codeForm" :rules="loginRules" class="login-form" auto-complete="on" label-position="left">

        <div class="title-container">
          <h1 class="title">Change Password</h1>
        </div>

        <div class="title-input">
          <h3 class="title">Verification Code:</h3>
        </div>

        <el-row :span="24">
          <el-col :span="13">
            <el-form-item prop="code">
              <el-input ref="code" v-model="codeForm.code" auto-complete="off" placeholder="Please enter the code" size="" />
            </el-form-item>
          </el-col>
          <el-col :span="11">
            <el-button type="primary" class="code-btn" :disabled="!show" @click="getCode()">
              <span v-show="show">Get verification code </span>
              <span v-show="!show"> Resend in {{ count }} s </span>
            </el-button>
          </el-col>
        </el-row>

        <div class="title-input">
          <h3 class="title">New Password:</h3>
        </div>
        <el-form-item prop="epassword">
          <span class="svg-container">
            <svg-icon icon-class="password" />
          </span>
          <el-input
            :key="passwordType"
            ref="epassword"
            v-model="codeForm.epassword"
            :type="passwordType"
            placeholder="Please enter the new password"
            name="epassword"
            tabindex="2"
            auto-complete="on"
          />
        </el-form-item>

        <div class="title-input">
          <h3 class="title">Repeat Password:</h3>
        </div>
        <el-form-item prop="epassword2">
          <span class="svg-container">
            <svg-icon icon-class="password" />
          </span>
          <el-input
            :key="passwordType"
            ref="epassword2"
            v-model="codeForm.epassword2"
            :type="passwordType"
            placeholder="Please repeat the password"
            name="epassword2"
            tabindex="2"
            auto-complete="on"
          />
        </el-form-item>

        <el-button :loading="loading" type="primary" style="width:100%;margin-bottom:30px;" @click.native.prevent="handleResetByCode">
          Confirm
        </el-button>

        <el-button type="primary" style="width:100%;margin-left:-1px;" @click.native.prevent="cancel()">
          Cancel
        </el-button>
        <div class="tips" style="margin-left: 30px;">
          <span style="margin-right:70px;">Email not available?</span>
          <a class="asp" @click="changeMethod()">Use password</a>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script>
import { sendVerification, resetPassword, resetPasswordWithOld } from '@/api/resetPassword'

export default {
  //change password page for a logged in user
  // two methods: email verification code or old password
  name: 'ChangePassword',
  data() {
    var validatePass2 = (rule, value, callback) => {
      if (value !== this.pswForm.password) {
        callback(new Error('Password does not match!'))
      } else {
        callback()
      }
    } //two new passwords must be the same
    const validateCode = (rule, value, callback) => {
      if (value !== this.identifyCode) {
        callback(new Error('Wrong verification code'))
      } else {
        callback()
      }
    }//email verification code must be correct
    const validateePass2 = (rule, value, callback) => {
      if (value !== this.codeForm.epassword) {
        callback(new Error('Password does not match!'))
      } else {
        callback()
      }//two new passwords must be the same
    }
    return {
      codeForm: {
        code: '',
        epassword: '',
        epassword2: ''
      }, //change through email verification code
      loginRules: { //input rules
        code: [
          { required: true, message: 'Verification code can not be empty', trigger: 'blur' },
          { validator: validateCode, trigger: 'blur' }
        ],
        epassword: [
          {
            required: true,
            message: 'Password cannot be empty',
            trigger: 'blur'
          },
          {
            min: 6,
            max: 12,
            message: 'Range within 6 to 12 characters',
            trigger: 'blur'
          }
        ],
        epassword2: [
          {
            required: true,
            message: 'Confirm password cannot be empty',
            trigger: 'blur'
          },
          {
            min: 6,
            max: 12,
            message: 'Range within 6 to 12 characters',
            trigger: 'blur'
          },
          {
            validator: validateePass2,
            trigger: 'blur'
          }
        ]
      },
      pswForm: {
        oldPassword: '',
        password: '',
        password2: ''
      }, //change through old password
      pswRules: {//input rules
        oldPassword: [
          {
            required: true,
            message: 'Password cannot be empty',
            trigger: 'blur'
          }
        ],
        password: [
          {
            required: true,
            message: 'Password cannot be empty',
            trigger: 'blur'
          },
          {
            min: 6,
            max: 12,
            message: 'Range within 6 to 12 characters',
            trigger: 'blur'
          }
        ],
        password2: [
          {
            required: true,
            message: 'Confirm password cannot be empty',
            trigger: 'blur'
          },
          {
            min: 6,
            max: 12,
            message: 'Range within 6 to 12 characters',
            trigger: 'blur'
          },
          {
            validator: validatePass2,
            trigger: 'blur'
          }
        ]
      },
      loading: false,
      passwordType: 'password',
      redirect: undefined,
      identifyCode: '',
      show: true,
      count: '',
      timer: null,
      showEmail: false,
      email: ''
    }
  },
  watch: {
    $route: {
      handler: function(route) {
        this.redirect = route.query && route.query.redirect
      },
      immediate: true
    }
  },
  mounted() {
    this.identifyCode = ''
    this.email = this.$store.state.user.email
  }, //emial is stored for a logged in user

  methods: {
    handleResetByCode() { //reset by verification code
      this.$refs.codeForm.validate(valid => {
        if (valid) {
          this.loading = true
          resetPassword(this.email, this.codeForm.epassword).then(res => { //call API
            this.loading = false
            if (res.data['success']) {
              this.$message({
                message: 'Reset Password Successfully',
                type: 'success'
              })
              this.$store.dispatch('user/logout') //log out the user and redirect to login page
              this.$router.push(`/login?redirect=${this.$route.fullPath}`)
            } else {
              this.$alert('Reset Password Failed. Please Try Again')
            }
          }).catch(error => {
            console.log(error)
            this.loading = false
          })
        } else {
          return false // error
        }
      })
    },
    handlePasswordReset() { //reset by old password
      this.$refs.pswForm.validate(valid => {
        if (valid) {
          this.loading = true
          resetPasswordWithOld(this.email, this.pswForm).then(res => { //call API
            this.loading = false
            if (res.data['success']) {
              this.$message({
                message: 'Reset Password Successfully',
                type: 'success'
              })
              this.$store.dispatch('user/logout') //log out the user and redirect to login page
              this.$router.push(`/login?redirect=${this.$route.fullPath}`)
            } else {
              this.$alert('Wrong Password! Please try again')
              this.loading = false
            }
          }).catch(error => {
            console.log(error)
            this.loading = false
          })
        } else {
          return false
        }
      })
    },
    getCode() {
      sendVerification(this.email).then(res => {
        // send verification code to the user email address
        console.log('---personal center-change password: get verification code successfully---')
        // console.log(res)
        if (res.data['success']) {
          this.$alert("We've sent you an email. Please check your email to find the verification code")
          this.identifyCode = res.data['code']
          if (!this.timer) {
            this.count = 60
            this.show = false
            this.timer = setInterval(() => {
              if (this.count > 0 && this.count <= 60) {
                this.count--
              } else {
                this.show = true
                clearInterval(this.timer)
                this.timer = null
              }
            }, 1000) //resend in 60 seconds, counter counts down every 1 second (1000 ms).
          }
        } else {
          this.$alert('System Busy! Please try again')
        }
      })
    },
    cancel() {
      this.$router.back()
    },
    changeMethod() {
      this.showEmail = !this.showEmail
    }
  }
}
</script>

<style lang="scss">
/* 修复input 背景不协调 和光标变色 */
/* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */

$bg:#283443;
$light_gray:#283443;
$cursor: #283443;

/* reset element-ui css */
.login-container {
  .el-input {
    display: inline-block;
    height: 47px;
    width: 85%;

    input {
      background: transparent;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      height: 47px;

      &:-webkit-autofill {
        box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-text-fill-color: $cursor !important;
      }
    }
  }

  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    color: #252525;
  }
}
</style>

<style lang="scss" scoped>
$bg:#2d3a4b;
$dark_gray:#2d3a4b;
$light_gray:#2d3a4b;
a:hover {  color : #409EFF ; }

.code-btn {
position: relative;
width: 100%;
font-size:14px;
margin-left: 10px;
}

.login-container {
  min-height: 100%;
  width: 100%;
  overflow: hidden;

  .login-form {
    position: relative;
    width: 520px;
    max-width: 100%;
    padding: 160px 35px 0;
    margin: 0 auto;
    overflow: hidden;
  }

  .tips {
    font-size: 14px;
    color: rgb(24, 22, 22);
    margin-top: 20px;

    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
    asp {
      margin-right:5px;
      cursor: pointer;
    }
  }

  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
  }

  .title-container {
    position: relative;

    .title {
      font-size: 48px;
      color: $light_gray;
      margin: 0px auto 30px auto;
      text-align: center;
      font-weight: bold;
    }
  }

  .title-input {
    position: relative;

    .title {
      font-size: 26px;
      color: $light_gray;
      margin: 20px auto 10px auto;
      text-align: left;
      font-weight: bold;
    }
  }

  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
  }
}
</style>
