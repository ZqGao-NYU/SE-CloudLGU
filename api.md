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
**Send**
- userEmai: User's Email

**Return**
- goodMail: bool (check the existance of mail, if true, then the mail is ok to register, and the verification code will be sent to the user's email)


#### Send Verification (Modify Password)
**Send**
- userEmail: User's Email

**Return**
- goodMail: bool (check the existance of mail, if true, then 

#### Forget Password
**Send**
- userEmail: user's email - string (Check its pattern in front-end, like xxx@link.cuhk.edu.cn and xxx@cuhk.edu.cn) 

**Return**
- sucess:  bool (success or failure, check the existance of the user's email)

  
#### Login 
**Send**
- userEmail: user's email - string (Check its pattern in front-end, like xxx@link.cuhk.edu.cn and xxx@cuhk.edu.cn) 
- password: password - string (Check its pattern in front-end. Only _digits_, _underline_, _alphabet_ are valid)

**Return**
- sucess:  bool (success or failure, check the correctness of the user's email and password)
- userInfo:{  
  identity: String (Faculty, Student, Administer)
  userID: int (Userr's ID in Database)  
}  

---

### _Admin (For Adminisiter)_
#### Get User Lists
**Send**
- Nothing  

**Return**
- id_list: list of users' id {Array of string}
- mail_list: list of users' email {Array of string}

#### Reset User Lists
**Send**
- userID: user's id
- userEmail: user's email

**Return**
- sucess:  bool (success or failure of the reset operation)
---
### _Profile_
#### Get Profile Info
**Send**
- userID: int (User's ID sent from the back-end) 

**Return**
- useName: User's Name {string}
- userEmail: User's Email {string}
- userIntro: User's self-introduction {string}
- userPhoto: User's profile photo {JPG/PNG}

#### Update User Introduction
**Send**
- userIntro: Updated user's self-introduction {string}  

**Return**
- sucess:  bool (success or failure of the update operation)

#### Update User Profile Photo
**Send**
- userPhoto: Updated user's profile photo {JPG/PNG}

**Return**
- sucess:  bool  (success or failure of the update operation)

---
### _Office Time Part_
### Create Office Time Slot 
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

### Delete Office Time Slot
**Send**
- otID: Office time ID of the office time slot to delete (ID)


**Return**
- success: bool (success or failure of the create operation)


### Update Office Time Slot
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

### Book Office Time
**Send** 
- otID: Office time ID got from the Database (Int)
- StudentID: Student ID who books the office time. (Int)

**Return**
- success: bool (success or failure of the book operation)

### Search by professor's name
**Send** 
- Professor_Name: Professor's Username given by the user

**Return**
- successs: bool (success or failure of the search opearation (no research result))
- List of info{  
  otID,  
  otStartTime,  
  otEndTime,  
  otLocation,  
  status (whether the slot is booked)  
}  

### Professor Check Office Time
**Send**
- Professor_ID: Professor's userID


**Return**
- List of info{  
  otID,  
  otStartTime,  
  otEndTime,  
  otLocation,  
  status (whether the slot is booked)  
}  
- success: bool (success or failure of the opearation)


---
### _Post Article_
### Create New Post
**Send**
- postTitle: Title of the post (String)
- postContent: Content of the post (String)
- postTag: Subject (Tag) of this post (String? **待定**)
- userID: Poster's ID (Int)

**Return** 
- postID: Poster's ID (Int)
- success: bool (success or failure of the create operation)  

### Delete Post
**Send**
- postID: Poster's ID (Int)

**Return**
- success: bool (success or failure of the delete operation)  

### Update Post
**Send**
- postID: Poster's ID (Int)
- postTitle: New title of the post (String)
- postContent: New content of the post (String)
- postTag: New Subject of this post (String? **待定**)

**Return** 
- postID: Updated Poster's ID (Int)
- success: bool (success or failure of the create operation)  

---
### _Comment Part_
### Create New Comment
**Send**
- postID: post's ID (Int)
- userID: Commenter's ID (Int)
- commentContent: Content of the comment (String)

**Return**
- commentID: Comment's ID (Int, with the foreign key Post ID)
- success: bool (success or failure of the create operation)  

### Delete Comment 
**Send**
- commentID: Content of the comment

**Return**
- success: bool (success or failure of the delete operation)  

### Update New Comment 
**Send**
- postID: post's ID (Int)
- commentID: Comment's ID (Int, with the foreign key Post ID)
- commentContent: Updated Content of the comment (String)

**Return**
- success: bool (success or failure of the update operation)  
