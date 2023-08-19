Travel Blog developed using flask and jinja2 template

Travel Blog where users can register , and then login , and post blogs about their travel experiences and add media such as photos and videos as well.

```run.py``` is used to run the application

```__init__.py``` conatins the part where app is initilialized as an object of Flask class, and other variables are defined

```routes.py``` contains route for

1. home
2. account
3. login
4. logout
5. register
6. map (incomplete)
7. new post
8. view specific post
9. update specific post
10. delete specific post
11. check all posts of a certain user

models.py contains db models , in our case it is a pretty simple db design with only 2 tables ,User and Post , with Post having foreign key which is userid of User table indicating a one to many relationship, i.e one User can have many posts forms.py which contains forms (classes) inherited from FlaskForm and other various other classes to help make the forms. The forms are

1. Registration Form
2. Login Form
3. Update Account Form
4. Post Form
5. Request Reset Form
6. Reset Password Form
Application also has various .html representing the routes mentioned above
