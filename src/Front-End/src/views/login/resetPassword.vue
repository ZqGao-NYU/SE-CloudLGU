<template>
  <div class="login-container">
    <div v-show="!showReset" class="login-container">
      <el-form ref="loginForm" :model="loginForm" :rules="loginRules" class="login-form" auto-complete="on" label-position="left">

        <div class="title-container">
          <h1 class="title">Reset Password</h1>
        </div>

        <div class="title-input">
          <h3 class="title">Email:</h3>
        </div>
        <el-form-item prop="email">
          <span class="svg-container">
            <svg-icon icon-class="email" />
          </span>
          <el-input
            ref="email"
            v-model="loginForm.email"
            placeholder="@(link.)cuhk.edu.cn"
            name="email"
            type="text"
            tabindex="1"
            auto-complete="on"
          />
        </el-form-item>

        <div class="title-input">
          <h3 class="title">Verification Code:</h3>
        </div>

        <el-row :span="24">
          <el-col :span="13">
            <el-form-item prop="code">
              <el-input ref="code" v-model="loginForm.code" auto-complete="off" placeholder="Please enter the code" size="" @keyup.enter.native="handleLogin" />
            </el-form-item>
          </el-col>
          <el-col :span="11">
            <el-button type="primary" class="code-btn" :disabled="!show" @click="getCode()">
              <span v-show="show">Get verification code </span>
              <span v-show="!show"> Resend in {{ count }} s </span>
            </el-button>
          </el-col>
        </el-row>

        <el-button :loading="loading" type="primary" style="width:100%;margin-bottom:30px;" @click.native.prevent="handleLogin">
          Next Step
        </el-button>

        <el-button type="primary" style="width:100%;margin-left:-1px;" @click.native.prevent="cancel()">
          Cancel
        </el-button>
      </el-form>
    </div>

    <div v-show="showReset" class="login-container">
      <el-form ref="pswForm" :model="pswForm" :rules="pswRules" class="login-form" auto-complete="on" label-position="left">

        <div class="title-container">
          <h1 class="title">Change Password</h1>
        </div>

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

        <el-button type="primary" style="width:100%;margin-bottom:30px;" @click.native.prevent="handleReset()">
          Confirm
        </el-button>

        <el-button type="primary" style="width:100%;margin-left:-1px;" @click.native.prevent="cancel()">
          Cancel
        </el-button>
      </el-form>
    </div>

  </div>

</template>

<script>
import { sendVerification, resetPassword } from '@/api/resetPassword'

export default {
  name: 'ResetPassword',
  data() {
    var validatePass2 = (rule, value, callback) => {
      if (value !== this.pswForm.password) {
        callback(new Error('Password does not match!'))
      } else {
        callback()
      }
    }
    const validateemail = (rule, value, callback) => {
      const end1 = value.slice(value.length - 17, value.length)
      const end2 = value.slice(value.length - 12, value.length)
      if (end1 !== '@link.cuhk.edu.cn' && end2 !== '@cuhk.edu.cn') {
        callback(new Error('Wrong email format: must be CUHKSZ email'))
      } else {
        callback()
      }
    }
    const validateCode = (rule, value, callback) => {
      if (value !== this.identifyCode) {
        callback(new Error('Wrong verification code'))
      } else {
        callback()
      }
    }
    return {
      loginForm: {
        email: '',
        code: ''
      },
      loginRules: {
        email: [{ required: true, trigger: 'blur', validator: validateemail }],
        code: [{ required: true, message: 'Verification code can not be empty', trigger: 'blur' }, { validator: validateCode, trigger: 'blur' }]
      },
      pswForm: {
        password: '',
        password2: ''
      },
      pswRules: {
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
      showReset: false
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
  },

  methods: {
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.showReset = true
        } else {
          return false // 登录失败提示错误
        }
      })
    },
    handleReset() {
      this.$refs.pswForm.validate(valid => {
        if (valid) {
          resetPassword(this.loginForm.email, this.pswForm.password).then(res => {
            if (res.data['success']) {
              this.$message({
                message: 'Reset Password Successfully',
                type: 'success'
              })
              this.$router.push('/login')
            } else {
              this.$alert('Reset Password Failed. Please Try Again')
            }
          }).catch(error => {
            console.log(error)
          })
        } else {
          return false
        }
      })
    },
    getCode() {
      const value = this.loginForm.email
      var end1 = value.slice(value.length - 17, value.length)
      var end2 = value.slice(value.length - 12, value.length)
      if (end1 !== '@link.cuhk.edu.cn' && end2 !== '@cuhk.edu.cn') {
        this.$alert('Invalid email format!')
      } else {
        sendVerification(this.loginForm.email).then(res => {
          console.log('---reset password: get verification code successfully---')
          console.log(res)
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
              }, 1000)
            }
          } else {
            this.$alert('Invalid Email!')
          }
        })
      }
    },
    cancel() {
      this.$router.back()
    }
  }
}
</script>

<style lang="scss">
/* 修复input 背景不协调 和光标变色 */
/* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */

$bg:#283443;
$light_gray:#fff;
$cursor: #fff;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .login-container .el-input input {
    color: $cursor;
  }
}

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
      color: $light_gray;
      height: 47px;
      caret-color: $cursor;

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
    color: #454545;
  }
}
</style>

<style lang="scss" scoped>
$bg:#2d3a4b;
$dark_gray:#889aa4;
$light_gray:#eee;
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
  background-color: $bg;
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
    color: #fff;
    margin-bottom: 10px;

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
