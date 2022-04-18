import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/adduser',
    component: () => import('@/views/login/adduser'),
    hidden: true
  },

  {
    path: '/resetPassword',
    component: () => import('@/views/login/resetPassword'),
    hidden: true
  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },

  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: 'Cloud LGU', icon: 'education' }
    }]
  },
  {
    path: '/forum',
    component: Layout,
    redirect: '/forum/all',
    name: 'forum',
    meta: { title: 'Forum', icon: 'message' },
    children: [
      {
        path: 'all',
        name: 'forum/All',
        component: () => import('@/views/forum/PostList'),
        meta: { title: 'All Posts', icon: 'list' }
      },
      {path: 'addPost',
      name: 'add_post',
      component: () => import('@/views/forum/addPost')
    },
      {
        path: 'post:postID',
        name: 'post_content',
        component: () => import('@/views/forum/Article'),
        params: {postID: '1'}
        }
    ]
  },
  // forum here, every one can access the forum

]

/**
 * asyncRoutes
 * the routes that need to be dynamically loaded based on user roles
 */
export const asyncRoutes = [
  {
    path: '/officetime',
    component: Layout,
    redirect: '/officetime/student/searchWeek',
    name: 'officetime',
    meta: { title: 'Office Time', icon: 'education', roles: ['admin','faculty','student'] },
    children: [
      {
        path: 'student/searchWeek',
        name: 'studentSearchWeek',
        component: () => import('@/views/ot/otStudentSearchWeek'),
        meta: { title: 'Search Week', icon: 'table',roles: ['admin','student'] }
      },
      {
        path: 'student/seachProf',
        name: 'studentSearchProf',
        component: () => import('@/views/ot/otStudentSearchProf'),
        meta: { title: 'Search Faculty', icon: 'search',roles: ['admin','student'] },
        params: {message: 'p1'}

      },
      {
        path: 'faculty',
        name: 'faculty',
        component: () => import('@/views/ot/otProfessor'),
        meta: { title: 'My Office Time', icon: 'eye-open',roles: ['admin','faculty'] }
      },
      {
        path: 'student/my',
        name: 'studentMy',
        component: () => import('@/views/ot/otStudentMy'),
        meta: { title: 'My', icon: 'people',roles: ['admin','student'] }
      }
    ]
  },
  {
    path: '/personalCenter',
    component: Layout,
    redirect: '/personalCenter/basicInfo',
    name: 'PersonalCenter',
    meta: { title: 'Personal Center', icon: 'user', roles: ['admin','faculty','student'] },
    children: [
      {
        path: 'basicInfo',
        name: 'BasicInfo',
        component: () => import('@/views/personalCenter/basicInfo'),
        meta: { title: 'Basic Infomation', icon: 'form', roles: ['admin','faculty','student'] }
      },
      {
        path: 'changePassword',
        name: 'ChangePassword',
        component: () => import('@/views/personalCenter/changePassword'),
        meta: { title: 'Change Password', icon: 'password', roles: ['admin','faculty','student'] }
      }
    ]
  },
  {
    path: '/manageUsers',
    component: Layout,
    redirect: '/manageUsers/manage',
    name: 'Manage Users',
    meta: {
      title: 'Manage Users',
      icon: 'peoples',
      roles: ['admin']
    },
    children: [
      {
        path: 'manage',
        name: 'Manage',
        component: () => import('@/views/manageUser/index'),
        meta: { title: 'Manage Users', icon: 'peoples'}
      }
    ]
  },

  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
