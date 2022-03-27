### API Design for CloudLGU
**The design of the APIs bases on the UML Class Diagram**
![UML Class](./images/Class_Diagram.png)  
---
### Login and Registration Part

#### Registrate
**Send**

- user's email - string (Check its pattern in front-end, like xxx@link.cuhk.edu.cn and xxx@cuhk.edu.cn) 
- password - string (Check its pattern in front-end. Only _digits_, _underline_, _alphabet_ are valid)
- password confirm - string (Check in front-end, whether the two passwords are identical)

**Return**
- confirmation status - string (success or failure, check the existance of the user)

---  

#### Forget Password
**Send**
- user's email - string (Check its pattern in front-end, like xxx@link.cuhk.edu.cn and xxx@cuhk.edu.cn) 

**Return**
- confirmation status - string (success or failure, check the existance of the user)

---  
#### Login 
**Send**
- user's email - string (Check its pattern in front-end, like xxx@link.cuhk.edu.cn and xxx@cuhk.edu.cn) 
- password - string (Check its pattern in front-end. Only _digits_, _underline_, _alphabet_ are valid)

**Return**
- confirmation status - string (success or failure, check whether the password and username are correct )
- identity - string （Staff, Students, Administer)


