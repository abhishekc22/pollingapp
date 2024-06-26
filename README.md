# pollingapp
I'd like to provide an overview of the polling app project I've developed, along with its working process, as outlined below:

Functionality Overview:

The polling app allows users to log in and participate in polls.
Users can view all available polls, regardless of whether they have a deadline or not.
Poll creators have the option to set deadlines for their polls, but participation is not restricted based on deadlines.
Each poll can have multiple choices, and users can only select one option per question for voting.
Technical Details:

The app is built using Django, and it leverages Django's admin interface for managing polls and user accounts.
User authentication is implemented using Django's built-in authentication system.
Polls are created with the ability to add multiple choices, and the voting process ensures that users can only select one option per question.
Future Enhancements:

Given sufficient time, I plan to refine the admin interface to provide more granular permissions for poll creation.
Additionally, I aim to enhance the user experience by implementing features such as real-time result updates and notifications.