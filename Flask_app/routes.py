from flask import Flask, render_template, url_for, flash, redirect , request, abort
from Flask_app import app , db , bcrypt , mail
from Flask_app.forms import *
from Flask_app.models import *
from flask_login import login_user , current_user , logout_user , login_required
import secrets
import os
from PIL import Image
from werkzeug.datastructures import FileStorage
from flask_mail import Message


@app.route("/")
@app.route("/home")
def home():
    no_of_images = []
    no_of_videos = []
    #posts = Post.query.all()
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page ,per_page=4)
    for post in posts:
        no_of_images.append(post.image.count(',') )
        no_of_videos.append(post.video.count(',') )
    return render_template('home.html', posts=posts ,  no_of_images = no_of_images , no_of_videos = no_of_videos)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created, an email has been sent to you as well ! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data): # if user exists and passwords match or not 
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home')) # redirect to next page if next page exists , else redirect to home 
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture,page):
    picture_fn_str_lst = ''
    if page == 'account':
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

        output_size = (125, 125)
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(picture_path)

        return picture_fn
    else:
        for picturee in form_picture:
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(picturee.filename) # get file extension 
            picture_fn = random_hex + f_ext
            picture_fn_str_lst += picture_fn +','

            picture_path = os.path.join(app.root_path, 'static/post_pics', picture_fn)
            output_size = (500 , 500)
            i = Image.open(picturee)
            i.thumbnail(output_size)
            i.save(picture_path)

        return picture_fn_str_lst

def save_video(form_video):
    #video_fn = ''
    video_fn_str_lst = ''
    video_fn_lst = []
    for videoo in form_video:
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(videoo.filename) # get file extension 
        video_fn = random_hex + f_ext
        video_fn_str_lst += video_fn + ','
        video_fn_lst.append(video_fn)
        video_path = os.path.join(app.root_path, 'static/post_videos', video_fn)
        videoo.save(video_path)

    return video_fn_str_lst




@app.route("/account",  methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    print(f"Form picture data  in account route {form.picture.data} ,  {form.picture}")
    page= 'account'
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data,page)
            current_user.image = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated! ', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file  = url_for('static', filename='profile_pics/' + current_user.image)
    return render_template('account.html', title='Account', image_file = image_file , form= form  )


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    page = 'new post' 
    if form.validate_on_submit():
        if form.picture.data[0].filename != '': # photo is uploaded
            print("Posted picture for form !!!")
            picture_file = save_picture(form.picture.data,page)
        if form.video.data[0].filename != '': # video is uploaded
            print("Posted video on form !!! ")
            video_file = save_video(form.video.data)

        if form.picture.data[0].filename != '' and form.video.data[0].filename != '':
            post=  Post(title = form.title.data, content = form.content.data, author= current_user, image = picture_file, video = video_file)
        elif form.picture.data[0].filename != '' and form.video.data[0].filename == '':
            post=  Post(title = form.title.data, content = form.content.data, author= current_user, image = picture_file)
        elif form.picture.data[0].filename == '' and form.video.data[0].filename != '':
            post=  Post(title = form.title.data, content = form.content.data, author= current_user, video = video_file)
        elif form.picture.data[0].filename == '' and form.video.data[0].filename == '':
            print("inside last elif !! ")
            post=  Post(title = form.title.data, content = form.content.data, author= current_user)

        db.session.add(post)
        db.session.commit()

        flash('Your post has been created ! ', 'success')
        return redirect(url_for('new_post'))
    return render_template('create_post.html', title='New Post' , form = form, legend = 'New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    no_of_images = post.image.count(',')
    no_of_videos = post.video.count(',')
    return render_template('post.html', title=post.title, post=post, no_of_images = no_of_images , no_of_videos = no_of_videos)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    page = 'update post'
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            print("Posted picture for form !!!")
            picture_file = save_picture(form.picture.data,page)
            post.image = picture_file

        if form.video.data:
            video_file = save_video(form.video.data)
            post.video = video_file
            print("posted video for form !!! in update form ")
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
    no_of_images = []
    no_of_videos = []
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    for post in posts:
        no_of_images.append(post.image.count(',') )
        no_of_videos.append(post.video.count(',') )
    return render_template('user_posts.html', posts=posts, user=user, no_of_images = no_of_images , no_of_videos = no_of_videos)

@app.route("/maps")
def maps():
    return render_template('map.html')

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender=os.environ.get('EMAIL_USER'),
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)