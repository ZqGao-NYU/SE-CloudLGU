import request from '@/utils/request'

// APIs related to reset password of an user

// request to send a email with verification code to user email
// will also return the verification code to fron-end for input checking
export function sendVerification(email) {
  return request({
    url: '/api/forget',
    method: 'post',
    data: {
      userEmail: email
    }
  })
}

// API to reset the password directly
// only available if the user inputs the correct verification code
//  i.e. the user is indeed the owner of the email
// send email and new password
// return status
export function resetPassword(email, psw) {
  return request({
    url: '/api/reset',
    method: 'post',
    data: {
      userEmail: email,
      password: psw
    }
  })
}

// API to rest the password by old password
// available for login user
// the user should input the old password and new password
// back-end would check the correctness of the old password
// return status: whether or not the modification is successfull
export function resetPasswordWithOld(email, pswForm) {
  return request({
    url: '/api/modifyPwd/old',
    method: 'post',
    data: {
      userEmail: email,
      oldPassword: pswForm.oldPassword,
      newPassword: pswForm.password
    }
  })
}
