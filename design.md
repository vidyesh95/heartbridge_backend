# **HeartBridge \- Design**

This document provides the technical design for the HeartBridge.

## **1\. System Architecture & Technology Stack**

* **Backend Framework:** Python 3.13 with a web framework like FastAPI or Django.  
* **Database:** PostgreSQL for its robustness and support for various data types.  
* **Password Hashing:** bcrypt library.  
* **Token Standard:** JSON Web Tokens (JWT) for session management.  
* **OAuth Providers:** Google and Apple.

## **2\. Database Schema Design**

We will need the following tables to manage users and their roles.

### **users table**

This table stores the core information for all users.

| Column Name | Data Type | Constraints | Description |
| :---- | :---- | :---- | :---- |
| id | UUID | PRIMARY KEY | Unique identifier for the user. |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User's email address. |
| password\_hash | VARCHAR(255) | NULLABLE | Hashed password for email/password auth. NULL for OAuth users. |
| auth\_provider | VARCHAR(50) | NOT NULL | The method used for registration ('email', 'google', 'apple'). |
| provider\_id | VARCHAR(255) | NULLABLE | Unique ID from the OAuth provider (e.g., Google's sub claim). |
| is\_verified | BOOLEAN | DEFAULT FALSE | Flag to check if the user's email is verified. |
| created\_at | TIMESTAMPZ | NOT NULL | Timestamp of account creation. |
| updated\_at | TIMESTAMPZ | NOT NULL | Timestamp of the last update. |

### **admins table**

This table stores information for administrators.

| Column Name | Data Type | Constraints | Description |
| :---- | :---- | :---- | :---- |
| id | UUID | PRIMARY KEY | Unique identifier for the admin. |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Admin's email address. |
| password\_hash | VARCHAR(255) | NOT NULL | Hashed password. |
| role | VARCHAR(50) | NOT NULL | Role of the admin ('super\_admin', 'moderator'). |
| mfa\_secret | VARCHAR(255) | NULLABLE | Secret key for Multi-Factor Authentication. |
| is\_mfa\_enabled | BOOLEAN | DEFAULT FALSE | Flag to check if MFA is set up and enabled. |
| created\_at | TIMESTAMPZ | NOT NULL | Timestamp of account creation. |
| updated\_at | TIMESTAMPZ | NOT NULL | Timestamp of the last update. |

## **3\. API Endpoint Design**

The following RESTful API endpoints will be created to handle authentication.

### **3.1. User Authentication Endpoints**

* POST /api/auth/register: Register a new user with email and password.  
  * **Request Body:** { "email": "user@example.com", "password": "strongpassword123" }  
  * **Response:** 201 Created with a success message. Sends a verification email.  
* POST /api/auth/login: Log in a user with email and password.  
  * **Request Body:** { "email": "user@example.com", "password": "strongpassword123" }  
  * **Response:** 200 OK with an access token and refresh token.  
* POST /api/auth/google: Handle Google OAuth callback.  
  * **Request Body:** { "token": "google\_auth\_token" }  
  * **Logic:** Verifies the token with Google. Creates a new user or logs in an existing one.  
  * **Response:** 200 OK with access and refresh tokens.  
* POST /api/auth/apple: Handle Apple OAuth callback.  
  * **Request Body:** { "token": "apple\_auth\_token" }  
  * **Response:** 200 OK with access and refresh tokens.  
* POST /api/auth/logout: Log out the current user.  
  * **Logic:** Invalidates the refresh token.  
  * **Response:** 200 OK.  
* POST /api/auth/refresh: Get a new access token using a refresh token.  
  * **Request Body:** { "refreshToken": "..." }  
  * **Response:** 200 OK with a new access token.  
* GET /api/auth/verify-email: Endpoint for the link sent to the user's email.  
  * **Query Params:** ?token=verification\_token  
  * **Response:** Redirects to a "verification successful" page.

### **3.2. Admin Authentication Endpoints**

* POST /api/admin/login: Log in an administrator.  
  * **Request Body:** { "email": "admin@heartbridge.com", "password": "adminpassword" }  
  * **Response:** 200 OK with a prompt for the MFA token.  
* POST /api/admin/verify-mfa: Verify the MFA token.  
  * **Request Body:** { "mfaToken": "123456" }  
  * **Response:** 200 OK with an admin access token.  
* POST /api/admin/logout: Log out the admin.  
  * **Response:** 200 OK.