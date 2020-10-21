from flask import Flask,render_template,url_for,flash,redirect,jsonify,request,session
from flask_sqlalchemy import SQLAlchemy
import os
import json
name=""

db_path=os.path.join(os.path.dirname(__file__))
db_uri='sqlite:///'+os.path.join(db_path,'dbfile.sqlite')


app=Flask(__name__)

app.config['SECRET_KEY'] = 'thisismysecretkeydonotstealit'
app.config['SQLALCHEMY_DATABASE_URI']=db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80))
    email=db.Column(db.String(80))
    password=db.Column(db.String(80))
    confirm_password=db.Column(db.String(80))
    mobile_number=db.Column(db.String(10))

db.create_all()

@app.route('/')
def homes():
    return render_template('index.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/add',methods=['GET','POST'])
def add():
    if request.method=='POST':
        name=request.form.get('user')
        email=request.form.get('email')
        password=request.form.get('pass')
        confirm_password=request.form.get('conpass')
        mobile_number=request.form.get('mobile')
        
        user = User.query.filter_by(name=name).first()
        if user:
            return render_template('sign.html')
        else:
            entry=User(name=name,email=email,password=password,confirm_password=confirm_password,mobile_number=mobile_number)
            db.session.add(entry)
            db.session.commit()
            # return redirect(url_for('start'))

            data="You've successfully enroll in our awesome app!"
            prop="alert alert-info"
            return render_template('signup.html',data=data,prop=prop)

    return render_template('signup.html')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':             
        email = request.form.get('email')
        name=email
        password = request.form.get('pass')
        user_name=User.query.filter_by(email=email).first()
        all_user=[]
        for i in User.query.order_by(User.email).all():
            all_user.append(i.email)
        print(all_user)
        if (email in all_user) and (password==user_name.password):
            return render_template("new.html",email=email)
        else:
            if (email in all_user) and (password!=user_name.password):
                return render_template('log.html')
            else:
                return render_template('false.html')


@app.route('/start')
def start():
    return render_template('new.html')

@app.route('/Area')
def Area():
    return render_template("prac.html")

@app.route('/adddata',methods=['GET','POST'])
def adddata():
    if request.method=="POST":
        area=request.form.get("arealabel")
        val=5
        data="Area Added Successfully!"
        prop="alert alert-info"
        org_data=None
        with open("data.json","r+") as f:
            org_data=json.loads(f.read())
            org_data.append({"Id":len(org_data)+1,"Name":area})
            f.seek(0)
            f.truncate()
            f.write(json.dumps(org_data,indent=4))
        print(org_data)
            
        return render_template("prac.html",area=area,val=val,data=data,prop=prop,org_data=org_data)
    return render_template("prac.html")


if __name__=="__main__":
    app.run(debug=True)