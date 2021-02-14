from flask import Flask, escape, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    application_name = "BikeService"
    return render_template('about.html', application_name=application_name)

@app.route('/hello/<message>')
def hello(message):
    return f'<h1>Welcome {escape(message)}</h1>'

@app.route('/blog_posts/<int:post_id>')
def display_blog_post(post_id):
    return f'<h1>Blog Post #{post_id}</h1>'
