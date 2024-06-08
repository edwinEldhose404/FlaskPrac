from flask import Flask, request, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Edwin'
app.config['MYSQL_DB'] = 'sample1'

mysql = MySQL(app)



@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        uname = request.form['username']
        uemail = request.form['email']

        cursor = mysql.connection.cursor()
        checker = 0
        for i in cursor:
            if i.key() == uname and i.value() == uemail:
                mysql.connection.commit()
                cursor.close()
                return f"Already Exists"
            elif i.key() == uemail:
                cursor.execute(" UPDATE example1 SET uemail = '%s' WHERE uname = '%s'",(uemail , uname))
                mysql.connection.commit()
                cursor.close()
                return f"Updated!"
        if checker == 1:
            cursor.execute(''' INSERT INTO example1 VALUES(%s,%s)''',(uname,uemail))
            mysql.connection.commit()
            cursor.close()
            return f"Done!!"
    return render_template('index.html')

@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    users = cur.execute('''SELECT * FROM example1''')

    if users > 0:
        users = cur.fetchall()
        return render_template('users.html',users=users)
    else:
        return render_template('users.html')

if __name__ == "__main__":
    app.run(debug=True)