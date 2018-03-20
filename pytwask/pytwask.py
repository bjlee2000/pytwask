#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime, time

from flask import Flask, flash, redirect, render_template, url_for

from forms import PostTweetForm, SignInForm, SignUpForm, ChangePasswordForm

app = Flask(__name__)

app.config['SECRET_KEY'] = b'c\x04\x14\x00;\xe44 \xf4\xf3-_9B\x1d\x15u\x02g\x1a\xcc\xd8\x04~'

# TODO: Read the real tweets from the backend Redis database.
tweets = [dict(username='renwei', time='2018-02-28 11:12:13', body='This is our first tweet!'),
          dict(username='htt', time='2018-03-01 23:00:00', body='This is our second tweet.')]

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SignInForm()
    if form.validate_on_submit():
        if form.check_login_credentials():
            return redirect(url_for('user_timeline', username=form.username.data, tweets=tweets))
        else:
            flash("Invalid username or passowrd")

    return render_template('index.html', form=form)


@app.route('/general_timeline')
def general_timeline():
    return render_template('timeline.html', tweets=reversed(tweets))


@app.route('/user_timeline', methods=['GET', 'POST'])
@app.route('/user_timeline/<username>', methods=['GET', 'POST'])
def user_timeline(username=None):
    form = PostTweetForm()
    if form.validate_on_submit():
        post_time = datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')
        tweets.append(dict(username='renwei', time=post_time, body=form.tweet.data))
        
        flash('Tweet successfully posted')
        return render_template('timeline.html', username=username, tweets=reversed(tweets), form=form)
    
    return render_template('timeline.html', username=username, tweets=reversed(tweets), form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        # TODO: Write the new user into the Redis database.
        print('New user {} created with password {}'.format(form.username.data, form.password.data))
        flash('Welcome, {}! Please login'.format(form.username.data))
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)


@app.route('/user_settings', methods=['GET', 'POST'])
def user_settings():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        # TODO: Write the new password into the Redis database.
        print('Password changed (old = {}, new = {})'.format(form.old_password.data, form.new_password.data))
    return render_template('user_settings.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500  


if __name__ == '__main__':
    app.run(debug=True)