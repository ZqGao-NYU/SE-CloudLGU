import request from '@/utils/request'

export function createOfficeTimeSlot(otForm) {
    return request({
      url: '/api/officetime/prof/create',
      method: 'post',
      data: {
        otDate: otForm.date,
        otStartTime: otForm.start,
        otEndTime: otForm.end,
        otLocation: otForm.location,
        Professor_userID: otForm.prof_id
      }
    })
  }

  export function deleteOfficeTimeSlot(id) {
    return request({
      url: '/api/officetime/prof/delete',
      method: 'post',
      data: {
        otID:id
      }
    })
  }

  export function bookOfficeTime(otID, StudentID) {
    return request({
      url: '/api/officetime/student/book',
      method: 'post',
      data: {
          otID: otID,
          StudentID: StudentID
      }
    })
  }

  export function searchProf(Professor_Name) {
    return request({
      url: '/api/officetime/student/searchprof',
      method: 'post',
      data: {
        Professor_Name:Professor_Name
      }
    })
  }

  export function searchWeek() {
    return request({
      url: '/api/officetime/student/searchtime',
      method: 'post'
    })
  }

  export function profCheckOfficeTime(Professor_ID) {
    return request({
      url: '/api/officetime/professor/show',
      method: 'post',
      data: {
        Professor_ID:Professor_ID
      }
    })
  } 
  
  export function studentCheckOfficeTime(Student_ID) {
    return request({
      url: '/api/officetime/student/show',
      method: 'post',
      data: {
        Student_ID:Student_ID
      }
    })
  }