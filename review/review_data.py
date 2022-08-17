#flak basics and create basic routes
from crypt import methods
from logging import root
from unicodedata import name
from flask import Flask,request, render_template, redirect,flash
# from flask import *
from db_config import get_db_connection
import re
# from flask_wtf import FlaskForm                      #
# from wtforms import StringField, TextAreaField, SubmitField
# from wtforms.validators import InputRequired, Email




app=Flask("__name1__")
app.secret_key="greeshma"

# class simpleform(FlaskForm):
#     submit=SubmitField("clicked")

def solve(s):
   pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
   if re.match(pat,s):
      return True
   return False

@app.route("/")
@app.route("/home")
def home():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM reviews;')
    data = cur.fetchall()
    print('data',data)
    conn.commit()
    flash('This is a flash message')

    # form= simpleform()
    # if form.validate_on_submit():
    #     flash("you cllicked the button")

    cur.close()
    conn.close()
    return render_template("home.html")

@app.route("/about")
def about():
    return "this is about page<h1>About</h1>"

@app.route('/reviews', methods =["GET", "POST"])
def review():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        # if solve(email):

        # email = StringField("Email",  [InputRequired("Please enter your email address."), Email("This field requires a valid email address")])

        review=request.form.get("review")
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO public.reviews (name, email, review)' 'VALUES(%s, %s, %s)', (name,email,review))
            # print("insertion return...................................",value1)
            # flash('This is a flash message')

        conn.commit()
        flash("Employee Inserted Successfully")
        cur.close()
        conn.close()
        return redirect('/lists')
        
    return render_template("post_data_new.html")
            


@app.route("/twitter",methods=["GET","POST"])
def twitter():
    if request.method == "GET":
        list2 =[]
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM public.twitter_data")
        list2=cur.fetchall()
        print(list2,"staert")
        conn.commit()
        cur.close()
        conn.close()
        print(list2)
    return render_template("list_tweetdata.html",lists=list2)  




@app.route("/lists",methods=["GET","POST"])
def list():
    if request.method == "GET":
        list2 =[]
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM public.reviews")
        list2=cur.fetchall()
        print(list2,"staert")
        conn.commit()
        cur.close()
        conn.close()
        print(list2)
    return render_template("listdata.html",lists=list2)  

@app.route("/delete/<int:id>",methods=["GET","POST"]) 
def delete(id):
    if request.method=="GET":
        conn=get_db_connection()
        cur=conn.cursor()
        cur.execute("DELETE from public.reviews where id="+str(id)) 
        conn.commit()
        cur.close()
        conn.close()
    return redirect('/lists')


@app.route("/update/<int:id>",methods=["GET","POST"])
def update(id):


    if request.method == "GET":
        result =[]
        conn=get_db_connection()
        cur=conn.cursor()
        query=cur.execute("select * from public.reviews where id="+str(id)) 
        result=cur.fetchone()
        # print("id:::::::::::;",result)
        conn.commit()
        cur.close()
        conn.close()
        return render_template("update.html",result=result)    
    
    if request.method=="POST":
        conn=get_db_connection()
        cur=conn.cursor()
        id=request.form.get("id")
        name=request.form.get("name")
        email=request.form.get("email")
        review=request.form.get("review")
        strSQl= "update public.reviews set name='"+name+"',email='"+email+"', review='"+review+"' where id="+str(id)
        # flash("you are successfuly updated in")
        cur.execute(strSQl)
        # data=cur.fetchall()
        # print("data................",data)
        conn.commit()
        cur.close()
        conn.close()
    return redirect('/lists')
    
if __name__=="__main__":
 app.run(debug=True)