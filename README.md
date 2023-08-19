# Travel_Blog
Travel Blog developed using flask and jinja2 template
Travel Blog developed using flask and jinja2 template

Travel Blog where users can register , and then login , and post blogs about their travel experiences and add media such as photos and videos as well.

```run.py``` is used to run the application

```__init__.py``` conatins the part where app is initilialized as an object of Flask class, and other variables are defined

```routes.py``` contains route for

home
account
login
logout
register
map (incomplete)
new post
view specific post
update specific post
delete specific post
check all posts of a certain user
models.py contains db models , in our case it is a pretty simple db design with only 2 tables ,User and Post , with Post having foreign key which is userid of User table indicating a one to many relationship, i.e one User can have many posts forms.py which contains forms (classes) inherited from FlaskForm and other various other classes to help make the forms. The forms are

Registration Form
Login Form
Update Account Form
Post Form
Request Reset Form
Reset Password Form
Application also has various .html representing the routes mentioned above

