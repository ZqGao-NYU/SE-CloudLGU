import request from '@/utils/request'

export function getAllUsers() {
  return request({
    url: '/api/admin/getList',
    method: 'post',
    data: {}
  })
}

export function resetProfile(editForm){
  const roles = [ ['admin'], ['faculty'], ['student'] ]
  return request({
    url: '/api/admin/resetProflie',
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

export function adminDeleteUser(email){
  return request({
    url: '/api/admin/deleteUser',
    method: 'post',
    data: {
      userEmail: email
    }
  })
}
