import request from '@/utils/request'

// APIs related to basic user functions

// login API
// user can login by email and password
// return a token that can uniquely identify the user
// the token is then stored to Cookies
export function login(loginForm) {
  return request({
    url: '/api/login',
    method: 'post',
    data: {
      userEmail: loginForm.email.trim(),
      password: loginForm.password
    }
  })
}

// register API
// for register, only user name, user email and password 
//  are required.
// No empty space allowed in user name
export function register(registerForm) {
  return request({
    url: '/api/register',
    method: 'post',
    data: {
      userName: registerForm.name.replace(/\s*/g, ''),
      userEmail: registerForm.email,
      password: registerForm.password
    }
  })
}

// send email verification code to user's email for register
// different with sendVerification in resetting password
// this is for unregistered user
// that one is for register user
// different requirements, different return messages
export function sendVerification(inemail) {
  console.log(inemail)
  return request({
    url: '/api/sendverification',
    method: 'post',
    data: { email: inemail.trim() }
  })
}

// get basic information (profile) of a user
// initially only token for the user was in Cookies
// use this API to the profile of the user
export function getInfo(token) {
  return request({
    url: '/api/getprofile',
    method: 'post',
    data: { token }
  })
}

