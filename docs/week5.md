### Jaakko:
Implemented notification API, did part of the final report.


## OWASP top ten week 5 considerations:
These are the week five security considerations tjat can be also found in the final report:

### A01:2021-Broken Access Control
There's only one type of user in our application and úsers can only modify item information of the items that they have put up for bidding.

### A02:2021-Cryptographic Failures
Only information that can be considered sensitive in our application is user passwords, that are hashed when saved to database.

### A03:2021-Injection
To prevent injection we are using MongoEngine, a document-object mapper for MongoDB, to handle the data.

### A04:2021-Insecure Design
While some basic security issues are addressed in our application, it's possible that there are some security risks caused by bad planning that we couldn’t find due to lack of time.

### A05:2021-Security Misconfiguration
This problem has been partially addressed by using the latest libraries. However, some of the Azure services were left open because configuring them would have taken a lot of time, an issue that probably would be bad to do in a real customer projects

### A06:2021-Vulnerable and Outdated Components
This issue is more of a problem when it comes to the upkeep of an application, thus is not something we considered in our project.

### A07:2021-Identification and Authentication Failures
Our application uses Flask-Login in order to combat this issue.

### A08:2021-Software and Data Integrity Failures
This issue has not been specifically addressed in our application, however we have not included unnecessary dependencies or libraries in the code.

### A09:2021-Security Logging and Monitoring Failures
We have implemented basic logging by using sentry.

### A10:2021-Server-Side Request Forgery
This issue has not been considered in our application.
