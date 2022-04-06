### API Design for CloudLGU
**The design of the APIs bases on the UML Class Diagram**
![UML Class](./images/Class_Diagram.png)  
---
### _Login and Registration Part_

#### Registrate
**Send**
- userName: user's name shown to other users - string (Check its pattern in front-end. Only _digits_, _underline_, _alphabet_ are valid)
- userEmail: user's email - string (Check its pattern in front-end, like xxx@link.cuhk.edu.cn and xxx@cuhk.edu.cn) 
- password: password - string (Check its pattern in front-end. Only _digits_, _underline_, _alphabet_ are valid. And check the password with the reenterred confirmaton password in advance)

**Return**
- goodMail: bool (check the existance of mail, if true, then the mail is ok to register)
- goodName: bool (check the existance of name, if ture, the name is ok to register)
- success: bool (if true, the register is finished, and the certification mail is sent to the email address. if false, goodMail or goodName may be False)


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
  isFaculty: bool (True for teacher, false for student)  
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
- otStartTime: Start Time of the wanted office time (String MM/DD/YYYY hh:mm)
- otEndTime: End time of the wanted office time (String MM/DD/YYYY hh:mm)
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
- otStartTime: Start Time of the wanted office time (String MM/DD/YYYY hh:mm)
- otEndTime: End time of the wanted office time (String MM/DD/YYYY hh:mm)
- otLocation: Where to hold the office time. (String)
- Professor_userID: Professor's userID (int sent from the backend during the login part)  
**Return**
- otID: New Office time ID stored in the Database (Int)  
- status:{  
  success: bool (success or failure of the create operation)  
  otherInfo: String (report success/failure reason (time conflict, location conflict))  
}  