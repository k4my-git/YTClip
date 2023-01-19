from flask import Flask, render_template, url_for, request, redirect
import getmeta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ydata.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    video_id = db.Column(db.String(20))
    uploader = db.Column(db.String(30))
    uploader_id = db.Column(db.String(20))
    view_count = db.Column(db.Integer)
    like_count = db.Column(db.Integer)
    upload_day = db.Column(db.String(10))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        posts = Post.query.order_by(Post.id.desc()).all()
        return render_template('index.html', posts=posts)
    else:
        url = request.form.get('url')
        if 'youtu' not in url:
            return redirect('/')
        data = getmeta.main(url)
        date = data['upload_date'][:4]+'/'+data['upload_date'][4:6]+'/'+data['upload_date'][6:]

        title = data['title']
        video_id = data['id']
        uploader = data['uploader']
        uploader_id = data['uploader_id']
        view_count = data['view_count']
        like_count = data['like_count']
        upload_day = date
        new_post = Post(title=title, video_id=video_id, uploader=uploader, uploader_id=uploader_id, view_count=view_count, like_count=like_count, upload_day=upload_day)

        db.session.add(new_post)
        db.session.commit()
        return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get(id)

    db.session.delete(post)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run()