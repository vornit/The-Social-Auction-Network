### Jaakko:
Implemented notification API, did part of the final report.

### Iiro:
Fixed several bugs in the app. Also prepared the pitch part of the presentation and the cost calculations for the final report.

### Renzo:
Wrote the features and used technologies listed and explained (use e.g. screenshots to illustrate)
Did the evaluation of meeting the client requirements

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

## Reported bugs and fixes

### Bug 1: Trying to login using non-registered email results in internal service error
#### Description
When trying to login using an email that is not registered, the app returns an internal service error.
#### Solution
Added check if the email returns None for the user and if so, an error message is shown.

### Bug 2: The system accepts bids under the winning bid
#### Description
It was possible to bid for an amount under the leading bid as long as it is higher than the starting bid.
#### Solution
Added check if the bid is higher than the leading bid.

### Bug 3: Item can be added with the starting price of 0 but it doesn't appear on item listing
#### Description
An item could be added with a starting price of 0 euros without an error message but the item doesn't appear on the item listing.
##### Solution
Fixed so that the form doesn't accept a starting price of 0.

### Bug 4: The price didn't update even when “Bid placed successfully!”
#### Description
When bidding for an item, the price didn't update even when “Bid placed successfully!” was shown.
#### Solution
Fixed the model of the bid (there were some definitions missing) so that the price of the item is updated correctly.

### Bug 5: Price with .0 causes error
#### Description
Adding an item to sell and adding the price with decimals with only zero caused an error.
#### Solution
Added another typecast in the form so that the price is taken from the form as a float.

### Bug 6: Clicking on items gives Internal Server Error
#### Description
Clicking on the name of the listed items generated an Internal Server Error
#### Solution
Added checks for Null values for leading bids so that the app won't crash.

### Bug 7: Missing empty title proper error
#### Description
When adding an item without a title, the app returned a very technical error message: "Error updating item: ValidationError (Item:63f0cd8d225a29d1c0f894fe) (String value is too short: ['title'])".
#### Solution
Fixed so that the form doesn't allow an empty title.