<template>
  <div class="login-container">
    <el-form ref="loginForm" :model="loginForm" :rules="loginRules" class="login-form" auto-complete="off" label-position="left">

      <div class="title-container">
        <h1 class="title">Cloud LGU</h1>
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
        <h3 class="title">Password:</h3>
      </div>
      <el-form-item prop="password" auto-complete="off">
        <span class="svg-container">
          <svg-icon icon-class="password" />
        </span>
        <el-input
          :key="passwordType"
          ref="password"
          v-model="loginForm.password"
          :type="passwordType"
          placeholder="Please enter password"
          name="password"
          tabindex="2"
          auto-complete="off"
        />
        <span class="show-pwd" @click="showPwd">
          <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'" />
        </span>
      </el-form-item>

      <div class="title-input">
        <h3 class="title">Verification Code:</h3>
      </div>

      <el-row :span="24">
        <el-col :span="13">
          <el-form-item prop="code">
            <el-input ref="code" v-model="loginForm.code" auto-complete="off" placeholder="Please enter the code" size="" @keyup.enter.native="handleLogin">
            </el-input>
          </el-form-item>  
        </el-col>
        <el-col :span="11">
          <div style="width:100%;margin-left:15px;margin-top:5px;" @click="refreshCode">
            <validation-code :identifyCode="identifyCode"></validation-code>
            </div>
        </el-col>
        </el-row>

      <el-button :loading="loading" type="primary" style="width:100%;margin-bottom:30px;" @click.native.prevent="handleLogin">
        LOGIN
      </el-button>

      <div class="tips" style="margin-left: 30px;">
        <span style="margin-right:20px;">Don't have an accont ?</span>
        <a class="asp" @click="goadduser">Create an account</a>
      </div>
      <div class="tips" style="margin-left: 30px;">
        <span style="margin-right:20px;">Forgot your password?</span>
        <a class="asp" @click="goreset">Reset password</a>
      </div>
    </el-form>
  </div>
</template>

<script>
import ValidationCode from './validationcode.vue'

export default {
  name: 'Login',
  components: {ValidationCode},
  data() {
    const validateEmail = (rule, value, callback) => {
      const end1 = value.slice(value.length - 17, value.length)
      const end2 = value.slice(value.length - 12, value.length)
      if (end1 !== '@link.cuhk.edu.cn' && end2 !== '@cuhk.edu.cn') {
        callback(new Error('Wrong email format: must be CUHKSZ email'))
      } else {
        callback()
      }
    }
    const validatePassword = (rule, value, callback) => {
      if (value.length < 6) {
        callback(new Error('The password can not be less than 6 digits'))
      } else {
        callback()
      }
    }
    const validateCode = (rule, value, callback) => {
      if (value.toLowerCase() !== this.identifyCode.toLowerCase()) {
        callback(new Error('Wrong verification code'))
        this.refreshCode()
      } else {
        callback()
      }
    }
    return {
      loginForm: {
        email: '',
        password: '',
        code: ''
      },
      loginRules: {
        email: [{ required: true, trigger: 'blur', validator: validateEmail }],
        password: [{ required: true, trigger: 'blur', validator: validatePassword }],
        code: [{required: true, message: 'Verification code can not be empty', trigger: 'blur'}, {validator: validateCode, trigger: 'blur'}]
      },
      loading: false,
      passwordType: 'password',
      redirect: undefined,
      identifyCodes: '012345679abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
      identifyCode: '',
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
    this.makeCode(this.identifyCodes, 4)
  },

  methods: {
    showPwd() {
      if (this.passwordType === 'password') {
        this.passwordType = ''
      } else {
        this.passwordType = 'password'
      }
      this.$nextTick(() => {
        this.$refs.password.focus()
      })
    },
    goadduser() {
      this.$router.push('/adduser')
    },
    goreset() {
      this.$router.push('/resetPassword')
    },
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.loading = true
          this.$store.dispatch('user/login', this.loginForm).then(() => {
            this.$router.push('/') // 登录成功之后重定向到首页
            this.loading = false
          }).catch((error) => {
            this.$alert("Invalid user email or password")
            console.log(error);
            this.loading = false
            this.refreshCode()
          })
        } else {
          console.log('error submit!!')
          this.refreshCode()
          this.passwordType = ''
          return false // 登录失败提示错误
        }
      })
    },
    refreshCode () {
      this.identifyCode = ''
      this.makeCode(this.identifyCodes, 4)
    },
    makeCode (o, l) {
      for (let i = 0; i < l; i++) {
        this.identifyCode += this.identifyCodes[this.randomNum(0, this.identifyCodes.length)]
      }
    },
    randomNum (min, max) {
      return Math.floor(Math.random() * (max - min) + min)
    },
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
