import Cookies from 'js-cookie'

const TokenKey = 'CloudLGU_token'

// token methods through Cookies
// get user token from Cookies
export function getToken() {
  return Cookies.get(TokenKey)
}

// set user token to Cookies
export function setToken(token) {
  return Cookies.set(TokenKey, token)
}

// remove user token from Cookies
export function removeToken() {
  return Cookies.remove(TokenKey)
}
