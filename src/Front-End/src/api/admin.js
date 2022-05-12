import request from '@/utils/request'
// API requests for admin only

// get the list of all users' information
// return user's email, name, introduction, password and identity
export function getAllUsers() {
  return request({
    url: '/api/admin/getList',
    method: 'post',
    data: {}
  })
}

// reset one particular user's profile
// user is uniquely identified by her/his email
// return whether the modification is successfully or not
export function resetProfile(editForm) {
  const roles = ['admin', 'faculty', 'student']
  return request({
    url: '/api/admin/resetProfile',
    method: 'post',
    data: {
      userEmail: editForm.email,
      userName: editForm.username,
      userIntro: editForm.intro,
      userPassword: editForm.password,
      userIdentity: roles[editForm.role_radio]
    }
  })
}

// delete one user
// user is uniquely identified by email
// return whether the deletion is successfully or not
export function adminDeleteUser(email) {
  return request({
    url: '/api/admin/deleteUser',
    method: 'post',
    data: {
      userEmail: email
    }
  })
}
