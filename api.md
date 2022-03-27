### API Design for CloudLGU
**The design of the APIs bases on the UML Class Diagram**
![UML Class](./images/Class_Diagram.png)  
---
### _Login and Registration Part_

#### Registrate
**Send**
- uID: user's ID - string (Check its pattern in front-end. Only _digits_, _underline_, _alphabet_ are valid)
- uEmail: user's email - string (Check its pattern in front-end, like xxx@link.cuhk.edu.cn and xxx@cuhk.edu.cn) 
- uPass: password - string (Check its pattern in front-end. Only _digits_, _underline_, _alphabet_ are valid)
- uPassConfirm: password confirm - string (Check in front-end, whether the two passwords are identical)

**Return**
- status: confirmation status - string (success or failure, check the existance of the user's ID and Email)

---  

#### Forget Password
**Send**
- uEmail: user's email - string (Check its pattern in front-end, like xxx@link.cuhk.edu.cn and xxx@cuhk.edu.cn) 

**Return**
- status: confirmation status - string (success or failure, check the existance of the user)

---  
#### Login 
**Send**
- uEmail: user's email - string (Check its pattern in front-end, like xxx@link.cuhk.edu.cn and xxx@cuhk.edu.cn) 
- uPass: password - string (Check its pattern in front-end. Only _digits_, _underline_, _alphabet_ are valid)

**Return**
- status: confirmation status - string (success or failure, check whether the password and username are correct )
- identity: identity - string （Staff, Students, Administer)

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
- uID: user's id
- uEmail: user's email

**Return**
- status: confirmation status - string  

---
### _Profile_
#### Get Profile Info
**Send**
- Nothing

**Return**
- uID: User's ID {string}
- uEmail: User's Email {string}
- uIntro: User's self-introduction {string}
- uPhoto: User's profile photo {JPG/PNG}

#### Update User Introduction
**Send**
- uIntro: Updated user's self-introduction {string}
**Return**
- status: Confirmation Status {bool}(Success)

#### Update User Profile Photo
**Send**
- uPhoto: User's profile photo {JPG/PNG}
**Return**
- status: Confirmation Status {bool}(Success)
