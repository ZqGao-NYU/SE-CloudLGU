import { login, getInfo } from '@/api/user'
import { getToken, setToken, removeToken } from '@/utils/auth'
import { resetRouter } from '@/router'

const getDefaultState = () => {
  return {
    token: getToken(),
    name: '',
    email: '',
    intro: '',
    avatar: '',
    roles: []
  }
}

const state = getDefaultState()

const mutations = {
  RESET_STATE: (state) => {
    Object.assign(state, getDefaultState())
  },
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_NAME: (state, name) => {
    state.name = name
  },
  SET_EMAIL: (state, email) => {
    state.email = email
  },
  SET_INTRO: (state, intro) => {
    state.intro = intro
  },
  SET_AVATAR: (state, avatar) => {
    state.avatar = avatar
  },
  SET_ROLES: (state, roles) => {
    state.roles = roles
  }
}

const actions = {
  // user login
  login({ commit }, loginForm) {
    return new Promise((resolve, reject) => {
      login(loginForm).then(res => {
        console.log('---login---store/user.js:login---')
        console.log(res);
        if (res.data['success']){
          commit('SET_TOKEN', res.data['token'])
          setToken(res.data['token'])
          resolve()
        } else{
          reject('login failed')
        }
      }).catch(error =>{
        reject(error)
      })
    })
  },

  // get user info
  getInfo({ commit, state }) {
    return new Promise((resolve, reject) => {
      getInfo(state.token).then(res => {
        console.log('---store/user.js: getInfo---');
        console.log(res);

        if (!res.data) {
          reject('Verification failed, please Login again.')
        }

        var role = [res.data['userIdentity']]

        //roles must be a non-empty array
        if (!role || role.length <= 0) {
          reject('getInfo: roles must be a non-null array!')
        }

        commit('SET_ROLES', role)
        commit('SET_NAME', res.data['userName'])
        commit('SET_EMAIL', res.data['userEmail'])
        commit('SET_INTRO', res.data['userIntro'])
        commit('SET_AVATAR', res.data['userPhoto'])
        resolve(role)
      }).catch(error => {
        reject(error)
      })
    })
  },

  // user logout
  logout({ commit}) {
    return new Promise(resolve => {
      removeToken() // must remove  token  first
      resetRouter()
      commit('RESET_STATE')
      resolve()
    })
  },

  // remove token
  resetToken({ commit }) {
    return new Promise(resolve => {
      removeToken() // must remove  token  first
      commit('RESET_STATE')
      resolve()
    })
  },
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}

