from flask import Flask, request, render_template, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '--INSERT PASSWORD HERE--'
app.config['MYSQL_DB'] = 'sample1'

mysql = MySQL(app)



@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        count = request.form['count']
        price = request.form['price']
        category = request.form['category']

        cursor = mysql.connection.cursor()
        
        cursor.execute(''' INSERT INTO inventory VALUES(%s,%s,%s,%s)''',(name,count,price,category))
        mysql.connection.commit()
        cursor.close()
        return f"Done!!"
        
    return render_template('index.html')

@app.route('/view')
def users():
    cur = mysql.connection.cursor()
    items = cur.execute('''SELECT * FROM inventory''')

    if items > 0:
        items = cur.fetchall()
        return render_template('items.html',items=items)
    else:
        return render_template('items.html')
    
@app.route('/edit',methods=['GET','POST'])
def manager():
    if request.method == 'POST':
        choice = request.form['choice']
        name = request.form['name']
        count = request.form['count']
        price = request.form['price']
        category = request.form['category']

        if choice == "del":
            cursor = mysql.connection.cursor()
            cursor.execute(''' DELETE FROM inventory WHERE name = %s ''',(name,))
            mysql.connection.commit()
            cursor.close()
        else:
            cursor = mysql.connection.cursor()
            cursor.execute(''' UPDATE inventory SET count = %s, price = %s, category = %s WHERE name = %s''',(count,price,category,name))
            mysql.connection.commit()
            cursor.close()
        

        return f"Done!!"
        
    return render_template('manager.html')

if __name__ == "__main__":
    app.run(debug=True)
