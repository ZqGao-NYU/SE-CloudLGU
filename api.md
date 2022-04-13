### API Design for CloudLGU
**The design of the APIs bases on the UML Class Diagram**
![UML Class](./images/Class_Diagram.png)  
---
### _Login and Registration Part_

#### Registrate
API Address: /api/register  

**Send**
- userName: user's name shown to other users - string (Check its pattern in front-end. Only _digits_, _underline_, _alphabet_ are valid)
- userEmail: user's email - string (Check its pattern in front-end, like xxx@link.cuhk.edu.cn and xxx@cuhk.edu.cn) 
- password: password - string (Check its pattern in front-end. Only _digits_, _underline_, _alphabet_ are valid. And check the password with the reenterred confirmaton password in advance)

**Return**
- goodMail: bool (check the existance of mail, if true, then the mail is ok to register)
- goodName: bool (check the existance of name, if ture, the name is ok to register)
- success: bool (if true, the register is finished, and the certification mail is sent to the email address. if false, goodMail or goodName may be False)
- status: string ("")

#### Send Verification (Register)
API Address: /api/sendverification  
**Send**
- userEmai: User's Email

**Return**
- goodMail: bool (check the existance of mail, if true, then the mail is ok to register, and the verification code will be sent to the user's email)  
- code(verification code)  

#### Send Verification (Modify Password)
API Address: /api/forget(same with forget password)  
**Send**
- userEmail: User's Email

**Return**
- goodMail: bool (check the existance of mail, if true, then the mail is ok to register, and the verification code will be sent to the user's email)  
- code(verification code)  

#### Forget Password
API Address: /api/forget  
**Send**
- userEmail: user's email - string (Check its pattern in front-end, like xxx@link.cuhk.edu.cn and xxx@cuhk.edu.cn) 

**Return**
- sucess:  bool (success or failure, check the existance of the user's email)  
- code: Verification Code

  
#### Login 
API Address: /api/login  
**Send**
- userEmail: user's email - string (Check its pattern in front-end, like xxx@link.cuhk.edu.cn and xxx@cuhk.edu.cn) 
- password: password - string (Check its pattern in front-end. Only _digits_, _underline_, _alphabet_ are valid)

**Return**
- sucess:  bool (success or failure, check the correctness of the user's email and password)
- token:{  
  identity: String (Faculty, Student, Administer)  
  userID: int (Userr's ID in Database)  
  info: string (Error Description)
}  

---

### _Admin (For Adminisiter)_  
API Address: /admin  
#### Get User Lists
**Send**
- Nothing  

**Return**
- id_list: list of users' id {Array of string}
- mail_list: list of users' email {Array of string}

#### Reset User Lists  
API Address: /api/reset  
**Send**
- userID: user's id
- userEmail: user's email

**Return**
- sucess:  bool (success or failure of the reset operation)
---
### _Profile_
#### Get Profile Info
API Address: /api/getprofile  
**Send**
- userID: int (User's ID sent from the back-end) 

**Return**
- useName: User's Name {string}
- userEmail: User's Email {string}
- userIntro: User's self-introduction {string}
- userPhoto: User's profile photo {JPG/PNG}

#### Update User Introduction
API Address: /api/updateprofile  
**Send**
- userIntro: Updated user's self-introduction {string}  

**Return**
- sucess:  bool (success or failure of the update operation)

#### Update User Profile Photo
API Address: /api/updateprofile  
**Send**
- userPhoto: Updated user's profile photo {JPG/PNG}

**Return**
- sucess:  bool  (success or failure of the update operation)

---
### _Office Time Part_
### Create Office Time Slot 
API Address: /api/officetime/prof/create  
**Send**
- otDate: Date of the office hour (String YYYY-MM-DD)
- otStartTime: Start Time of the wanted office time (String hh-mm)
- otEndTime: End time of the wanted office time (String hh-mm)
- otLocation: Where to hold the office time. (String)
- Professor_userID: Professor's userID (int sent from the backend during the login part)  


**Return**
- otID: Office time ID stored in the Database (Int)  
- status:{  
  success: bool (success or failure of the create operation)  
  otherInfo: String (report success/failure reason (time conflict, location conflict))  
}  

### Delete Office Time Slot(for teacher)
API Address: /api/officetime/prof/delete  
**Send**
- otID: Office time ID of the office time slot to delete (ID)


**Return**
- success: bool (success or failure of the create operation)


### Update Office Time Slot(for teacher)
API Address: /api/officetime/prof/update  
**Send**
- otID: Office time ID got from the Database (Int)
- otDate: Date of the Office Hour (String YYYY-MM-DD)
- otStartTime: Start Time of the wanted office time (String hh:mm)
- otEndTime: End time of the wanted office time (String hh:mm)
- otLocation: Where to hold the office time. (String)


**Return**  
- otID: New Office time ID stored in the Database (Int)  
- status:{  
  success: bool (success or failure of the create operation)  
  otherInfo: String (report success/failure reason (time conflict, location conflict))  
}  

### Book Office Time(for student)  
API Address: /api/officetime/student/book  
**Send** 
- otID: Office time ID got from the Database (Int)
- StudentID: Student ID who books the office time. (Int)

**Return**
- success: bool (success or failure of the book operation)

### Search by professor's name
API Address: /api/officetime/student/searchprof  
**Send** 
- Professor_Name: Professor's Username given by the user

**Return**
- successs: bool (success or failure of the search opearation (no research result))
- lists: [{  
  otID,  
  otStartTime,  
  otEndTime,  
  otLocation,  
  isBooked (whether the slot is booked),  
  booked_by
}] (List of Json Objects)   
### Search This Week
API Address: /api/officetime/student/searchtime   
**Send**  
- Nothing     
**Return**
- success: bool (If no professor hold OH this week, it will return False)
- lists:[  
  prof:{  
  profID: int Professor's User ID
  profName: String Professor's User Name
  }]  
### Professor Check Office Time
API Address: /api/officetime/professor/show  
**Send**
- Professor_ID: Professor's userID  

**Return**
- lists: [{  
  otID,  
  otStartTime,  
  otEndTime,  
  otLocation,  
  isbooked,
  booked_by,
}]     (List of json objects)  
- success: bool (success or failure of the opearation)  

### Student Check Office Time
API Address: /api/officetime/student/show  
**Send**
- Student_ID: Student's userID  

**Return**
- lists: [{  
  otID,  
  otStartTime,  
  otEndTime,  
  otLocation,  
  prof_name
}]     (List of json objects)
- success: bool (success or failure of the opearation)  



---
### _Post Article_
### Create New Post
API Address: /api/forum/post/create  
**Send**
- postTitle: Title of the post (String)
- postContent: Content of the post (String)
- postTag: Subject (Tag) of this post (String? **待定**)
- userID: Poster's ID (Int)

**Return** 
- postID: Post's ID (Int)
- success: bool (success or failure of the create operation)  

### Delete Post
API Address: /api/forum/post/delete  
**Send**
- postID: Poster's ID (Int)

**Return**
- success: bool (success or failure of the delete operation)  

### Update Post
API Address: /api/forum/post/update  
**Send**
- postID: Post's ID (Int)
- postTitle: New title of the post (String)
- postContent: New content of the post (String)
- postTag: New Subject of this post (String? **待定**)

**Return** 
- postID: Updated Poster's ID (Int)
- success: bool (success or failure of the create operation)  

### Show Post
API Address: /api/forum/post/show  
**Send**
- postID: Post's ID (Int)  

**Return**
- success: bool (success or failure of the delete operation)  
- postTitle: Title of the post (String)  
- postContent: Content of the post (String)  
- postTag: Subject of this post (String? **待定**)  
- posterName: Name of the poster(String)  
- createTime: Create time of the post(String)  
- updateTime: Last update time of the post(String)  
- commentList: All comments for this post(**具体细节待定**)  

### Show All Post
API Address: /api/forum/post/showall  
**Send**
- 不需要特别的send内容，因为是返回所有的post

**Return**
- success: bool (success or failure of the delete operation)  
- postList: All posts  
    --Title：Title of the post (String)  
    --Content：Content of the post (String)  
    --Tag: Subject of this post (String? **待定**)  
    --Poster: Name of the poster(String) 
    --Ctime: Create time of the post(String)  
    --UpdateTime: Last update time of the post(String)  

---
### _Comment Part_
### Create New Comment
API Address: /api/forum/comment/create 
**Send**
- postID: post's ID (Int)
- userID: Commenter's ID (Int)
- commentContent: Content of the comment (String)

**Return**
- commentID: Comment's ID (Int, with the foreign key Post ID)
- success: bool (success or failure of the create operation)  

### Delete Comment 
API Address: /api/forum/comment/delete  
**Send**
- commentID: Content of the comment

**Return**
- success: bool (success or failure of the delete operation)  

### Update New Comment  
API Address: /api/forum/comment/update
**Send**
- postID: post's ID (Int)
- commentID: Comment's ID (Int, with the foreign key Post ID)
- commentContent: Updated Content of the comment (String)

**Return**
- success: bool (success or failure of the update operation)  
