# Week 1

### Jaakko: 
Created gitlab.jyu.fi group, installed programs and did setup 
for local development, wrote and submited userstories to moodle and wrote 3 
OWASP considerations.

### Iiro:
Set up the project pipeline including Azure and Gitlab runner, set up the local environment and wrote one OWASP consideration.

### Pertti:
Set up the local development environment and wrote one OWASP consideration.

## OWASP top ten week 1 considerations:

### A07:2021 – Identification and Authentication Failures
It maybe important to consider making some sort of effort against 
Identification and Authentication Failures, when we are making system that
handles users money (example Auction System).

### A09:2021 - Security Logging and Monitoring Failures
All logins and login attempts should be logged to make it easier to investigate possible malicious login attempts.

### A03:2021 – Injection
Because the application is going to handle customer data, it is crucial to take measures to prevent injection. Primarily we
should make sure to use a safe API to make queries and handle the data.

### A01:2021 – Broken Access Control
It's important to make sure (possible) hackers don't have easy access to web-application data. All except public resources should be denied by default.

### A02:2021 – Cryptographic Failures
Auction system of course needs to handle and move sensitive data of it's customers,
all sensitive data should be encrypted.