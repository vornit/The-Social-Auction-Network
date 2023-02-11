### Iiro:
Did the basic logging setup and added SAST into the pipeline. Also implemented sharing items on social media.

## OWASP top ten week 3 considerations:

### A02:2021 – Cryptographic Failures
Auction system user passwords are hashed when saved to database.

### A07:2021 – Identification and Authentication Failures
It maybe important to consider making some sort of effort against Identification and Authentication Failures, when we are making system that handles users money (example Auction System). We try to make authentication safer by using Flask-Login.

### A09:2021 - Security Logging and Monitoring Failures
All logins and login attempts should be logged to make it easier to investigate possible malicious login attempts. We currently have implemented basic logging.

### A03:2021 – Injection
Because the application is going to handle customer data, it is crucial to take measures to prevent injection. To prevent injection we are using MongoEngine, a document-object mapper for MongoDB, to handle the data.

### A01:2021 – Broken Access Control
It's important to make sure (possible) hackers don't have easy access to web-application data. All except public resources should be denied by default. This should be kept in mind at all times.