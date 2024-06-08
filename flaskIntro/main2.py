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
