from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import desc

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
app.app_context().push()
# https://youtu.be/JsZ1C9O_2XE?si=37_ntE0MvU9E_IbR
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    like = db.Column(db.Integer, primary_key=False)
    dislike = db.Column(db.Integer, primary_key=False)
    comment = db.Column(db.String(500), nullable=False)
    writer = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime)
    def __repr__(self):
        return '<Task %r>' % self.id
    
@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        newcomment=request.form['CommentInput']
        newwriter=request.form['WriterInput']
        NewComment=Comment(comment=newcomment,writer=newwriter,like=0,dislike=0,date_created=datetime.utcnow())
        try:
            db.session.add(NewComment)
            db.session.commit()
            return redirect('/')
        except:
            return '<h1>'+str(datetime.utcnow())+'<h1>'
    else:
        # https://www.geeksforgeeks.org/using-request-args-for-a-variable-url-in-flask/
        SelectedKey = request.args.get('Key')
        Mode = request.args.get('Mode')
        OrderBy = request.args.get('OrderBy')
        if OrderBy=='None':
            OrderBy='Latest'
        if SelectedKey==None:
            SelectedKey=0
        if Mode ==None:
            # 'D' = Delete
            # 'U' = Update
            Mode='D'
        if OrderBy==None or OrderBy=='Latest':
            tasks=Comment.query.order_by(Comment.date_created).all()
        if OrderBy=='Oldest':
            tasks=Comment.query.order_by(desc(Comment.date_created)).all()
        if OrderBy=='ABCDEZ':
            tasks=Comment.query.order_by(Comment.writer).all()
        if OrderBy=='ZYXWVA':
            tasks=Comment.query.order_by(desc(Comment.writer)).all()
        if OrderBy=='Likess':
            tasks=Comment.query.order_by(Comment.like).all()

        # This line will return the first data (based on order by)
        #tasks=Comment.query.order_by(Comment.date_created).first()

        return render_template('index.html',tasks=tasks,SelectedKey=SelectedKey,Mode=Mode,OrderBy=OrderBy)

@app.route('/delete/<id>')
def delete(id):
    delete_task=Comment.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect('/')
    except:
        return 'Delete Problem'

@app.route('/update/<id>',methods=['GET','POST'])
def update(id):
    task=Comment.query.get_or_404(id)
    OrderBy = request.args.get('OrderBy')
    if OrderBy=='None':
        OrderBy='Latest'
    if request.method == 'POST':
        task.comment=request.form['UpdateInput']
        try:
            db.session.commit()
            return redirect('/?OrderBy='+OrderBy+'&Key=0')
        except:
            return 'Update Error'
    else:
        # https://www.geeksforgeeks.org/using-request-args-for-a-variable-url-in-flask/
        return redirect('/')


@app.route('/like/<id>',methods=['GET','POST'])
def like(id):
    task=Comment.query.get_or_404(id)
    OrderBy = request.args.get('OrderBy')
    if OrderBy=='None':
        OrderBy='Latest'
    Dislike = request.args.get('Dislike')
    if request.method == 'POST':
        if Dislike=='0':
            task.like+=1
        else:
            task.dislike+=1
        # Task.like is not updated.
        try:
            db.session.commit()
        except:
            return '<h1>Like Error<h1>'
        return redirect('/?OrderBy='+OrderBy)
    else:
        return redirect('/?OrderBy='+OrderBy)

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host="localhost", port=8000,debug=True)

'''
# https://stackoverflow.com/questions/73309491/port-xxxx-is-in-use-by-another-program-either-identify-and-stop-that-program-o
'''

'''
python3 app.py
'''