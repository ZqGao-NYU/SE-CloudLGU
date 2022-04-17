import request from '@/utils/request'

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

export function register(registerForm) {
  return request({
    url: '/api/register',
    method: 'post',
    data: {
      userName: registerForm.name,
      userEmail: registerForm.email,
      password: registerForm.password
    }
  })
}

export function sendVerification(inemail) {
  console.log(inemail)
  return request({
    url: '/api/sendverification',
    method: 'post',
    data: { email: inemail.trim() }
  })
}

export function getInfo(token) {
  return request({
    url: '/api/getprofile',
    method: 'post',
    data: { token }
  })
}

