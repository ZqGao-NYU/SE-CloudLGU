import request from '@/utils/request'
// APIs related to user modifing profile

// user can change his/her name and introduction
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

// user can also upload avatar
// Separate these two APIs since changing avatar
//  involves file exchange and the data may not 
//  be readily in the database
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
