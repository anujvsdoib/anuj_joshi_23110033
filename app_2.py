from os import name
from flask import Flask, redirect, url_for, request, Response, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='4440'
app.config['MYSQL_DB']='dcc_a4'
mysql = MySQL(app)

def get_data():
    cursor=mysql.connection.cursor()
    cursor.execute('select distinct Name_of_the_Purchaser from d11')
    name_of_purchaser=list(cursor.fetchall())
    name_of_purchaser.sort()
    cursor.close()
    cursor=mysql.connection.cursor()
    cursor.execute('select distinct name_of_p_party from d10')
    name_of_party=list(cursor.fetchall())
    name_of_party.sort()
    cursor.close()
    return name_of_purchaser,name_of_party

@app.route('/', methods = ["POST", "GET"])
def main_page():
    name_of_purchaser,name_of_party=get_data()
    return render_template("index.html",name_of_purchaser=name_of_purchaser,name_of_party=name_of_party)
bond_number=0
@app.route('/a_2', methods = ["POST", "GET"])
def a_2():
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        table_name=request.form['tablename']
        cursor.execute(f'select * from {table_name} where bond_number = %s',(request.form['box'],))
        data=cursor.fetchall()
        bond_number=request.form['box']
    if len(data)==0:
        return render_template('index.html',a_2_data = [['Not Found']])
    
    return render_template("e_1.html", a_2_data = data,filter=['Name of Purchaser','Name of Party'],bond_number=bond_number) 
@app.route('/e_1',methods=['POST','GET'])

def e_1():
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        table_name = request.form['tablename']
        column_name = request.form['filter_type']
        filter_value = request.form['filter_value']
        
        cursor.execute(f"SELECT * FROM {table_name} WHERE `{column_name}` = %s", (filter_value,))

        data = cursor.fetchall()
        cursor.close()
        
        return render_template('e_1.html', a_2_data=data, filter=['Name of Purchaser', 'Name of Party'])

    return redirect(url_for('main_page'))


@app.route('/e_2',methods=['POST','GET'])
def e_2():
    if request.method == "POST":
        cursor=mysql.connection.cursor()
        value=request.form['Company']
        
        cursor.execute("select bond_number, Denominations, year from d11 where Name_of_the_Purchaser = %s",(request.form['Company'],))
        data=cursor.fetchall()
        d = {}
        for row in data:
            bond_number = row[0]
            denominations = int(row[1].replace(',', ''))  
            year = row[2]
            d[year] = d.get(year, 0) + denominations
            cursor.close()
    if len(data)==0:
        return render_template('index.html',e_2_data = [['Not Found']])
    years=list(d.keys())
    amount=list(d.values())
    name_of_purchaser,name_of_party=get_data()
    return render_template('e_2.html',e_2_data = data,years=years,amount=amount)
        
@app.route('/e_3',methods=['POST','GET'])
def e_3():
    if request.method == "POST":
        cursor=mysql.connection.cursor()
        value=request.form['party']
        
        cursor.execute("select bond_number, Denominations, year from d10 where name_of_p_party= %s",(request.form['party'],))
        data = cursor.fetchall()
        d = {}
        for row in data:
            bond_number = row[0]
            denominations = int(row[1].replace(',', ''))  # Remove commas and convert to integer
            year = row[2]
            d[year] = d.get(year, 0) + denominations
        cursor.close()
    
    years=list(d.keys())
    amount=list(d.values())
    if len(data)==0:
        return render_template('index.html',e_3_data = [['Not Found']])
    name_of_purchaser,name_of_party=get_data()
    return render_template('e_3.html',e_3_data = data,years1=years,amount1=amount)

@app.route('/e_4',methods=['POST','GET'])
def e_4():
    if request.method=="POST":
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT bond_number, Name_of_the_Purchaser, Denominations FROM d11 WHERE bond_number IN (SELECT bond_number FROM d10 WHERE name_of_p_party  = %s)',(request.form['party'],))
        data=cursor.fetchall()
        
        if len(data)==0:
            return render_template('index.html',e_4_data = [['Not Found']])
        name_of_purchaser,name_of_party=get_data()
        d = {}
        for row in data:
            name_of_purchaser = row[1]
            denominations = int(row[2].replace(',', ''))  # Remove commas and convert to integer
            d[name_of_purchaser] = d.get(name_of_purchaser, 0) + denominations
        companies=list(d.keys())
        total_amount=list(d.values())
        return render_template('e_4.html',companies=companies,total_amount=total_amount,e_4_data = list(d.items()),party=request.form['party'])
@app.route('/e_5',methods=['POST','GET'])
def e_5():
    if request.method=="POST":
        cursor=mysql.connection.cursor()
        value=request.form['company']
        
        cursor.execute('SELECT name_of_p_party, Denominations FROM d10 WHERE bond_number IN (SELECT bond_number FROM d11 WHERE Name_of_the_Purchaser = %s)',(request.form['company'],))
        data=cursor.fetchall()
        if len(data)==0:
            return render_template('index.html',e_5_data = [['Not Found']])
       
        d = {}
        for row in data:
            name_of_party = row[0]
            denominations = int(row[1].replace(',', ''))  # Remove commas and convert to integer
            d[name_of_party] = d.get(name_of_party, 0) + denominations

        parties=list(d.keys())
        total_amount=list(d.values())
        total_denominations=sum(total_amount)
        name_of_purchaser,name_of_party=get_data()
        return render_template('e_5.html',e_5_data = list(d.items()),parties=parties,total_amount=total_amount,total_denominations=total_denominations,company=request.form['company'])

@app.route('/e_6',methods=['POST','GET'])

@app.route('/e_6', methods=['POST', 'GET'])
def e_6():
    if request.method == "POST":
        print(request.form['Pie Chart'])
        cursor = mysql.connection.cursor()
        cursor.execute('select Denominations, name_of_p_party from d10')
        data = cursor.fetchall()
        d = {}
        for i in range(len(data)):
            # Remove commas from the string and then convert to integer
            d[data[i][1]] = d.get(data[i][1], 0) + int(data[i][0].replace(',', ''))  
        print(d)
        party = list(d.keys())
        total_donations = list(d.values())
    return render_template('e_6.html', party=party, total_donations=total_donations)


if __name__ == '__main__':
   app.run(host="0.0.0.0", port="80", debug = True) 