import request from '@/utils/request'

export function updateProfile(token, editForm, file){
    return request({
        url: '/api/updateprofile',
        method: 'post',
        data:{
            token,
            userName: editForm.username,
            userIntro: editForm.intro,
            userPhoto: file
        }
    })
}