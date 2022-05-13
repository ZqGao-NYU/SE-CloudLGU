import request from '@/utils/request'
// APIs related to Office Time pages

// create a new OT record
// send: otDate,otStartTime:,otEndTime,otLocation,Professor_userID
// return: success or not
export function createOfficeTimeSlot(otForm) {
  return request({
    url: '/api/officetime/professor/create',
    method: 'post',
    data: {
      otDate: otForm.otDate,
      otStartTime: otForm.otStartTime,
      otEndTime: otForm.otEndTime,
      otLocation: otForm.otLocation,
      Professor_userID: otForm.Professor_userID
    }
  })
}

// delete an OT record
// send: otID
// return: success or not
export function deleteOfficeTimeSlot(id) {
  return request({
    url: '/api/officetime/professor/delete',
    method: 'post',
    data: {
      otID: id
    }
  })
}

// for student to book an available OT
// send: otID and studentID
// return: success or not
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

// for student to search a professor's OT information
// send: professor name
// return: all available OT of this professor,
//     include all information of each OT slot
export function searchProf(Name) {
  return request({
    url: '/api/officetime/student/searchprof',
    method: 'post',
    data: {
      Professor_Name: Name
    }
  })
}

// for student to get available professor in this week
// send: None
// because the result is queried by date and time now
// return: available professor's name in each day of week
export function searchWeek() {
  return request({
    url: '/api/officetime/student/searchtime',
    method: 'get'
  })
}

// for prof to see all information of existig OT
// send: professor ID got from website
// return: all OT form (booked and not booked)
export function profCheckOfficeTime(Professor_ID) {
  return request({
    url: '/api/officetime/professor/show',
    method: 'post',
    data: {
      Professor_ID: Professor_ID
    }
  })
}

// for student to check booked OT
// send: student ID got from website
// return: all OT form booked by this student
export function studentCheckOfficeTime(id) {
  return request({
    url: '/api/officetime/student/show',
    method: 'post',
    data: {
      Student_ID: id
    }
  })
}
