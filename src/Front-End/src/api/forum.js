import request from '@/utils/request'
// APIs related to forum pages

// get all data for a post when clicking in the post list
// send: post ID
// return: all information include
//    title, tag, content, posterName, create time, update time, comments
export function showPost(id) {
  return request({
    url: '/api/forum/post/show',
    method: 'post',
    data: {
      postID: id
    }
  })
}

// get a list of all posts
// use tags to divide posts into different list
// "All" list include all posts with any tags
// send: None
// return: post[], include 
//    postID, tag, title, content, posterName, createTime, updateTime 
export function showAllPost() {
  return request({
    url: '/api/forum/post/showall',
    method: 'post'
  })
}

// use when create new post record
// send: postForm: title, content, tag, posterID
// return: success or not
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

// use when create comment on a post
// send: commentForm: postID, commenterID, content
// return: success or not
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

// use to delete a comment record
// send: commentID
// return: success or not
export function deleteComment(id) {
  return request({
    url: '/api/forum/comment/delete',
    method: 'post',
    data: {
      commentID: id
    }
  })
}
