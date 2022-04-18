import request from '@/utils/request'

export function updateProfile(token, editForm) {
  return request({
    url: '/api/updateprofile',
    method: 'post',
    data: {
      userID: token,
      userName: editForm.username,
      userIntro: editForm.intro
    }
  })
}

export function updateAvatar(file) {
  return request({
    url: '/api/updatePhoto',
    method: 'post',
    data: file,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}
