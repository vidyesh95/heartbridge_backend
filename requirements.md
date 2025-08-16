# **HeartBridge \- Requirements**

This document outlines the functional and non-functional requirements for the authentication system of the HeartBridge website.

## **1\. User Authentication**

### **1.1. Functional Requirements**

* **User Registration:**  
  * Users must be able to create an account using:  
    * Google (OAuth 2.0)  
    * Apple (OAuth 2.0)  
    * Email and Password  
  * Upon registration via email, users must verify their email address by clicking a link sent to their inbox.  
  * Passwords must meet minimum complexity requirements (e.g., 8 characters, one uppercase, one lowercase, one number, one special character).  
* **User Login:**  
  * Users must be able to log in using their registered method (Google, Apple, or email/password).  
  * The system should provide a "Forgot Password" functionality for email-based users, allowing them to reset their password securely via an email link.  
  * The system should implement a mechanism to prevent brute-force attacks (e.g., rate limiting on login attempts).  
* **User Logout:**  
  * Authenticated users must have a clear and accessible way to log out.  
  * Logging out should invalidate the user's session token.  
* **Session Management:**  
  * User sessions should be managed using secure tokens (e.g., JWT \- JSON Web Tokens).  
  * Tokens should have a reasonable expiration time to enhance security.  
  * The system should support "Remember Me" functionality, which provides a longer-lived session for trusted devices.

### **1.2. Non-Functional Requirements**

* **Security:**  
  * All communication between the client and server must be encrypted using HTTPS.  
  * Passwords must be securely hashed (e.g., using bcrypt or Argon2) before being stored in the database.  
  * OAuth 2.0 implementation must follow best practices to prevent common vulnerabilities.  
* **Performance:**  
  * Authentication requests (login, registration) should be processed quickly, ideally under 500ms.  
* **Scalability:**  
  * The authentication system should be able to handle a growing number of users without significant performance degradation.

## **2\. Admin Authentication**

### **2.1. Functional Requirements**

* **Admin Login:**  
  * Administrators will have a separate, dedicated login portal.  
  * Admin accounts are created manually by super-admins, not through public registration.  
  * Admin authentication will be strictly via email and password.  
  * Admin accounts must have Multi-Factor Authentication (MFA) enabled (e.g., using an authenticator app like Google Authenticator).  
* **Role-Based Access Control (RBAC):**  
  * The system will support different admin roles (e.g., Super-Admin, Moderator, Support).  
  * Permissions and access to different parts of the admin dashboard will be restricted based on the administrator's role.

### **2.2. Non-Functional Requirements**

* **Security:**  
  * All admin-related endpoints must be strictly protected and require a valid admin session token.  
  * All administrative actions should be logged for auditing purposes.  
* **Usability:**  
  * The admin login process should be straightforward but highly secure.