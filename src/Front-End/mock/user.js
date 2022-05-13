
const tokens = {
  admin: {
    token: 'admin-token'
  },
  student: {
    token: 'student-token'
  },
  faculty: {
    token: 'faculty-token'
  }
}

const users = {
  'admin-token': {
    roles: ['admin'],
    introduction: 'I am a super administrator',
    avatar: 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
    name: 'Super Admin',
    email: 'admin@cuhk.edu.cn'
  },
  'student-token': {
    roles: ['student'],
    introduction: 'I am an student',
    avatar: 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
    name: 'Normal student',
    email: 'student@cuhk.edu.cn'
  },
  'faculty-token': {
    roles: ['faculty'],
    introduction: 'I am a professor',
    avatar: 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
    name: 'Normal professor',
    email: 'faculty@cuhk.edu.cn'
  }
}

module.exports = [
  // user login
  {
    url: '/vCloudLGU/user/login',
    type: 'post',
    response: config => {
      const { useremail } = config.body
      const token = tokens[useremail]

      // mock error
      if (!token) {
        return {
          code: 60204,
          message: 'Account and password are incorrect.'
        }
      }

      return {
        code: 20000,
        data: token
      }
    }
  },

  // get user info
  {
    url: '/vCloudLGU/user/info\.*',
    type: 'get',
    response: config => {
      const { token } = config.query
      const info = users[token]

      // mock error
      if (!info) {
        return {
          code: 50008,
          message: 'Login failed, unable to get user details.'
        }
      }

      return {
        code: 20000,
        data: info
      }
    }
  },

  // user logout
  {
    url: '/vCloudLGU/user/logout',
    type: 'post',
    response: _ => {
      return {
        code: 20000,
        data: 'success'
      }
    }
  }
]
