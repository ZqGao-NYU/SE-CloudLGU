import request from '@/utils/request'

export function sendVerification(email){
    return request({
        url: '/api/forget',
        method: 'post',
        data: {
            userEmail: email
        }
    })
}

export function resetPassword(email, psw){
    return request({
        url: '/api/reset',
        method: 'post',
        data:{
            userEmail: email,
            password: psw
        }
    })
}

export function resetPasswordWithOld(email, pswForm){
    return request({
        url: '/api/modifyPwd/old',
        method: 'post',
        data:{
            userEmail: email,
            oldPassword: pswForm.oldPassword,
            newPassword: pswForm.password
        }
    })
}