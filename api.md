### API Design for CloudLGU
**The design of the APIs bases on the UML Class Diagram**
![UML Class](./images/Class_Diagram.png)  
---
### _Login and Registration Part_

#### Registrate
**Send**
- userID: user's ID - string (Check its pattern in front-end. Only _digits_, _underline_, _alphabet_ are valid)
- userEmail: user's email - string (Check its pattern in front-end, like xxx@link.cuhk.edu.cn and xxx@cuhk.edu.cn) 
- password: password - string (Check its pattern in front-end. Only _digits_, _underline_, _alphabet_ are valid. And check the password with the reenterred confirmaton password in advance)

**Return**
- status: confirmation status - string (success or failure, check the existance of the user's ID and Email)

---  

#### Forget Password
**Send**
- userEmail: user's email - string (Check its pattern in front-end, like xxx@link.cuhk.edu.cn and xxx@cuhk.edu.cn) 

**Return**
- status: confirmation status - string (success or failure, check the existance of the user)

---  
#### Login 
**Send**
- userEmail: user's email - string (Check its pattern in front-end, like xxx@link.cuhk.edu.cn and xxx@cuhk.edu.cn) 
- password: password - string (Check its pattern in front-end. Only _digits_, _underline_, _alphabet_ are valid)

**Return**
- status: confirmation status - string (success or failure, check whether the password and username are correct )
- useridentity: identity - string （Staff, Students, Administer)

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
- status: confirmation status - string  

---
### _Profile_
#### Get Profile Info
**Send**
- Nothing

**Return**
- userID: User's ID {string}
- userEmail: User's Email {string}
- userIntro: User's self-introduction {string}
- userPhoto: User's profile photo {JPG/PNG}

#### Update User Introduction
**Send**
- userIntro: Updated user's self-introduction {string}
**Return**
- status: Confirmation Status {bool}(Success)

#### Update User Profile Photo
**Send**
- userPhoto: User's profile photo {JPG/PNG}
**Return**
- status: Confirmation Status {bool}(Success)
