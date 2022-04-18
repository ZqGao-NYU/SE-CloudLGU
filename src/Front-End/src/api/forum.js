import request from '@/utils/request'

export function showPost(id) {
    return request({
      url: '/api/forum/post/show',
      method: 'post',
      data: {
        postID:id
      }
    })
  }

  export function showAllPost() {
    return request({
      url: '/api/forum/post/showall',
      method: 'post'
    })
  }

  export function createPost(postForm) {
    return request({
      url: '/api/forum/post/create',
      method: 'post',
      data: {
        postTitle: postForm.postTitle,
        postContent: postForm.content,
        postTag: postForm.tag,
        userID: postForm.userID
      }
    })
  }

  export function createComment(commentForm) {
    return request({
      url: '/api/forum/comment/create',
      method: 'post',
      data: {
        postID: commentForm.postID,
        userID: commentForm.userID,
        commentContent: commentForm.commentContent
      }
    })
  }

    export function deleteComment(id) {
      return request({
        url: '/api/forum/comment/delete',
        method: 'post',
        data: {
          commentID: id
      }
    })
  }
