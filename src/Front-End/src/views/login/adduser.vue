<template>
  <div class="register">
    <section class="form-container">
      <span class="title">Create a CloudLGU Account</span>
      <div class="manage-tip">
        <el-form ref="registerForm" :model="registerUser" status-icon :rules="rules" label-width="100px" class="registerForm">
          <el-form-item label="Username" prop="name">
            <el-input v-model="registerUser.name" placeholder="Please input the username" />
          </el-form-item>
          <el-row :span="24">
            <el-col :span="14">
              <el-form-item label="Email" prop="email">
              <el-input v-model="registerUser.email" placeholder="Please input CUHKSZ email" />
              </el-form-item>
            </el-col>
            <el-col :span="10">
              <el-button type="primary" class="code-btn" @click="getCode()" :disabled="!show"> 
                <span v-show="show">Get verification code </span>
                <span v-show="!show"> Resend in {{ count }} s </span>  
              </el-button>
            </el-col> 
          </el-row>
          <el-form-item label="Code" prop="code">
            <el-input v-model="registerUser.code" placeholder="Please input the email verification code"/>
          </el-form-item>
          <el-form-item label="Password" prop="password">
            <el-input v-model="registerUser.password" type="password" placeholder="Please input the password" />
          </el-form-item>
          <el-form-item label="Confirm" prop="password2">
            <el-input v-model="registerUser.password2" type="password" placeholder="Confirm the password" />
          </el-form-item>
          <el-button type="primary" class="submit-btn" @click="submitForm()">Create new account</el-button>
          <el-button type="primary" class="log-btn" @click="signIn()">Already have an account? LOG IN</el-button>
        </el-form>
      </div>
    </section>
  </div>
</template>

<script>
import { register, sendVerification } from '@/api/user'

export default {
  name: 'Register',
  components: {},
  data() {
    var validatePass2 = (rule, value, callback) => {
      if (value !== this.registerUser.password) {
        callback(new Error('Password does not match!'))
      } else {
        callback()
      }
    }
    var validateEmail = (rule, value, callback) => {
      const end1 = value.slice(value.length - 17, value.length)
      const end2 = value.slice(value.length - 12, value.length)
      if (end1 !== '@link.cuhk.edu.cn' && end2 !== '@cuhk.edu.cn') {
        callback(new Error('Wrong email format: must be CUHKSZ email'))
      } else {
        callback()
      }
    }
    var validateCode = (rule, value, callback) => {
      if (value !== this.verifyCode){
        callback(new Error('Wrong email verification code'))
      } else {
        callback()
      }
    }

    return {
      registerUser: {
        name: '',
        email: '',
        code: '',
        password: '',
        password2: '',
      },
      verifyCode: '',
      show: true,
      count: '',
      timer: null,
      rules: {
        name: [
          {
            required: true,
            message: 'Username cannot be empty',
            trigger: 'blur'
          },
          {
            min: 5,
            max: 12,
            message: 'Range within 5 to 12 characters',
            trigger: 'blur'
          }
        ],
        email: [
          {
            type: 'email',
            required: true,
            message: 'Email cannot be empty',
            trigger: 'blur'
          },
          {
            validator: validateEmail,
            trigger: 'blur'
          }
        ],
        code: [
          {
            required: true,
            message: 'Verification code cannot be empty',
            trigger: 'blur'
          },
          {
            validator: validateCode,
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
      }
    }
  },

  mounted() {

  },

  methods: {
    submitForm() {
      this.$refs.registerForm.validate((valid) => {
        if (valid){
          register(this.registerUser).then(res => {
            if (res.data['success']){
              this.$message({
                message: 'Register Successfully',
                type: 'success'
              })
              this.$router.push("/login")
            } else{
              this.$alert("Email alerady registered!")
            }
          })
        }
      })
    },
    signIn() {
      this.$router.push('/login')
    },

    getCode(){
      let value = this.registerUser.email
      var end1 = value.slice(value.length - 17, value.length)
      var end2 = value.slice(value.length - 12, value.length)
      if (end1 !== '@link.cuhk.edu.cn' && end2 !== '@cuhk.edu.cn') {
        this.$alert("Invalid email format!")
      } else {
        sendVerification(this.registerUser.email).then(res => {
          console.log('---register: get verification code successfully---')
          //console.log(res)
          if (res.data['goodMail']){
            this.$alert("We've sent you an email. Please check your email to find the verification code, which is valid in 30 minutes")
            this.verifyCode = res.data['code']
            if (!this.timer){
              this.count = 60;
              this.show = false;
              this.timer = setInterval(()=> {
                if (this.count > 0 && this.count <= 60){
                  this.count --;
                } else{
                  this.show = true;
                  clearInterval(this.timer);
                  this.timer = null;
                }
              },1000)
            }
          } else {
            this.$alert('Email has already been registered!')
          }
        })
        
      }
    },
  },
}
</script>

<style lang="scss">
  .register{
    input {
      background: transparent;
      border: 2px;
      border-radius: 2px;
      padding: 12px 5px 12px 15px;
      color: #fff;
      height: 47px;
      caret-color: #fff;
    }
    label {
      color:#fff;
    }
  }

  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
    color: #454545;
  }
</style>


<style lang="scss" scoped>
.register {
  position: relative;
  width: 100%;
  height: 100%;
/*    background: url(url) no-repeat center center;*/
  background-size: 100% 100%;
  text-align: center;
  background: #283443;
}

.form-container {
  width: 50%;
  height: 210px;
  position: absolute;
  background-color: #283443; 
  top: 10%;
  left: 30%;
  padding: 25px;
  border-radius: 0;
  margin: 0 auto;
  text-align: center;
}

.title {
font-family: 'Microsoft TaHei';
font-weight: bold;
font-size: 26px;
color: #eee;
}

.registerForm {
width: 90%;
margin-top: 20px;
padding: 20px 40px 20px 20px;
border-radius: 5px;
/* margin-left: 40%; */
}

.submit-btn {
position: relative;
width: 70%;
background-color: #72246C;
}

.log-btn {
position: relative;
width: 70%;
font-size:14px;
margin-top: 20px;
margin-left: -2px;
}

.code-btn {
position: relative;
width: 80%;
font-size:14px;
}

.el-form-item {
    color: #454545;
}


</style>