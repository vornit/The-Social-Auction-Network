# Week 1

### Jaakko: 
Created gitlab.jyu.fi group, installed programs and did setup 
for local development, wrote and submited userstories to moodle and wrote 1 
OWASP consideration.

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