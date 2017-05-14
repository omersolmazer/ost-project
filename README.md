Open Source Tools final project

Project is deployed to Heroku, accessible through this link:
https://ost-reservation.herokuapp.com

To work locally, .env file is needed with Database settings configured.

Basically a Django project, configured in Python. Uses 3 models, 1 being the built-in User model from Django. The rest are for resource and reservation.
Uses standard heroku template for html rendering.


All functionalities working.

Here are the extras:
- Displaying number of times a resource has been reserved
- Search by name and tags
- Users can only have 1 reservation at a time
- Capacity for resources
