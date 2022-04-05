import logging
from flask import Flask, flash, redirect, request, render_template,  url_for, session
import pymysql

app = Flask(__name__)
app.config["DEBUG"]=True

db=pymysql.connect(host="localhost",port=3306,user="root",passwd="0430",db="parkingdb")

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.secret_key = 'B!1w8NAt1T^%kvhUI*S^'
app.config["DEBUG"]=True 
user = {"username": "paola", "password": "0430"}

@app.route('/',methods=['GET','POST'])
def index():
  if (request.method == 'POST'):
    username=request.form.get('username')
    password=request.form.get('password')
    if username==user['username'] and password==user['password']:
      session['user']=username
      return redirect ('/gestion_clientes')
    flash ("El usuario o la contraseña son incorrectos")
    return render_template('login.html')
  return render_template("login.html")

@app.route('/logout')
def logout():
    return redirect ('/')
    
   

@app.route('/gestion_clientes')
def gestion_clientes():
    return render_template('gestion_clientes.html')
 
 
@app.route('/clientes')
def clientes():
 cur=db.cursor(pymysql.cursors.DictCursor)
 cur.execute("select * from clientes")
 data=cur.fetchall()
 cur.close()
 return render_template('clientes.html',clientes=data)

@app.route('/editar_cliente/<id>',methods=['POST','GET'])
def editarcliente(id):
  cur=db.cursor(pymysql.cursors.DictCursor)
  datos=(id,)
  comando="select * from clientes where cliente_id= %s"
  cur.execute(comando,datos)
  data=cur.fetchall()
  cur.close()
  return render_template('editar_cliente.html',cliente=data[0])

@app.route('/update_cliente/<id>' ,methods=['POST' ])
def updatecliente(id):
  cliente_id= id
  primer_nombre= request.form['primer_nombre']
  primer_apellido= request.form['primer_apellido']
  tipo_cliente= request.form['tipo_cliente']
  cedula= request.form['cedula']
  telefono= request.form['telefono']
  email= request.form['email']
  cursor =db.cursor()
  comando="UPDATE clientes set primer_nombre = %s, primer_apellido = %s, tipo_cliente = %s, cedula = %s, telefono = %s, email = %s  where cliente_id = %s"
  datos=(primer_nombre, primer_apellido, tipo_cliente, cedula, telefono, email, cliente_id)
  cursor.execute(comando, datos)
  flash('Cliente actualizado exitosamente')
  db.commit()
  return redirect(url_for('clientes'))

@app.route('/new_cliente', methods=['POST', 'GET'])
def new_cliente():
  return render_template('agregar_cliente.html')
  
@app.route('/agregar_cliente',methods=['POST'])
def agregarcliente():
  primer_nombre= request.form['primer_nombre']
  primer_apellido= request.form['primer_apellido']
  tipo_cliente= request.form['tipo_cliente']
  cedula= request.form['cedula']
  telefono= request.form['telefono']
  email= request.form['email']
  cursor =db.cursor()
  comando=" INSERT INTO clientes (primer_nombre,primer_apellido,tipo_cliente,cedula,telefono,email) values (%s,%s,%s,%s,%s,%s)"
  datos=(primer_nombre, primer_apellido ,tipo_cliente,cedula,telefono,email)
  cursor.execute(comando,datos)
  flash('cliente agregados exitosamente')
  db.commit()
  return redirect(url_for('clientes'))

@app.route('/espacios')
def espacios():
 cur=db.cursor(pymysql.cursors.DictCursor)
 cur.execute("select * from espacios")
 data=cur.fetchall()
 cur.close()
 return render_template('espacios.html',espacios=data )

@app.route('/editar_espacio/<id>',methods=['POST','GET'])
def editarespacio(id):
 cur=db.cursor(pymysql.cursors.DictCursor)
 datos=(id,)
 comando="select * from espacios where espacio_id= %s"
 cur.execute(comando,datos)
 data=cur.fetchall()
 cur.close()
 return render_template('editar_espacio.html',espacio=data[0])

@app.route('/new_espacios', methods=['POST', 'GET'])
def new_espacios():
 return render_template('agregar_espacios.html')

@app.route('/agregar_espacios',methods=['POST'])
def agregarespacios():  
 lote_id= request.form['lote_id']
 tipo= request.form['tipo']
 disponible= request.form['disponible']
 costo_hora= request.form['costo_hora']
 cursor =db.cursor()
 comando=" INSERT INTO espacios (lote_id,tipo,disponible,costo_hora) values (%s,%s,%s,%s)"
 datos=(lote_id , tipo , disponible , costo_hora)
 cursor.execute(comando , datos)
 flash('Espacio agregado exitosamente')
 db.commit()
 return redirect(url_for('espacios'))

@app.route('/update_espacio/<id>' ,methods=['POST' ])
def updateespacios(id):
 espacio_id=id
 lote_id= request.form['lote_id']
 tipo= request.form['tipo']
 disponible= request.form['disponible']
 costo_hora= request.form['costo_hora']
 cursor =db.cursor()
 comando="UPDATE espacios set lote_id= %s, tipo= %s, disponible= %s, costo_hora= %s  where espacio_id= %s"
 datos=(lote_id,tipo,disponible,costo_hora,espacio_id)
 cursor.execute(comando,datos)
 flash('Espacio actualizado exitosamente')
 db.commit()
 return redirect(url_for('espacios'))

@app.route('/historicos')
def historicos():
 cur=db.cursor(pymysql.cursors.DictCursor)
 cur.execute("select * from historico")
 data=cur.fetchall()
 cur.close()
 return render_template('historicos.html',historico=data )


@app.route('/editar_historico/<id>',methods=['POST','GET'])
def editarhistorico(id):
 cur=db.cursor(pymysql.cursors.DictCursor)
 datos=(id,)
 comando="select * from historico where historico_id= %s"
 cur.execute(comando,datos)
 data=cur.fetchall()
 cur.close()
 return render_template('editar_historico.html',historico=data[0])

@app.route('/update_historico/<id>' ,methods=['POST' ])
def updatehistorico(id):
 historico_id=id
 espacio_id= request.form['espacio_id']
 fecha_entrada= request.form['fecha_entrada']
 fecha_salida= request.form['fecha_salida']
 pagado= request.form['pagado']
 placa= request.form['placa']
 cursor =db.cursor()
 comando="UPDATE historico set  espacio_id=%s, fecha_entrada = %s, fecha_salida = %s, pagado = %s, placa = %s  where historico_id = %s"
 datos=( espacio_id, fecha_entrada, fecha_salida, pagado, placa, historico_id)
 cursor.execute(comando, datos)
 flash('Historico actualizado exitosamente')
 db.commit()
 return redirect(url_for('historicos'))

@app.route('/new_historico', methods=['POST', 'GET'])
def new_historico():
 return render_template('agregar_historico.html')

@app.route('/agregar_historico',methods=['POST'])
def agregarhistorico(): 
  fecha_entrada= request.form['fecha_entrada']
  fecha_salida= request.form['fecha_salida']
  espacio_id= request.form['espacio_id']
  pagado= request.form['pagado']
  placa= request.form['placa']
  cursor =db.cursor()
  comando=" INSERT INTO historico (fecha_entrada,fecha_salida,espacio_id,pagado,placa) values (%s,%s,%s,%s,%s)"
  datos=(fecha_entrada,fecha_salida,espacio_id,pagado,placa)
  cursor.execute(comando,datos)
  flash('Historico agregado exitosamente')
  db.commit()
  return redirect(url_for('historicos'))


@app.route('/loteparqueo')
def loteparqueo():
 cur=db.cursor(pymysql.cursors.DictCursor)
 cur.execute("select * from loteparqueo")
 data=cur.fetchall()
 cur.close()
 return render_template('loteparqueos.html',loteparque=data )


@app.route('/editar_loteparq/<id>',methods=['POST','GET'])
def editarloteparqueo(id):
 cur=db.cursor(pymysql.cursors.DictCursor)
 datos=(id,)
 comando="select * from loteparqueo where lote_id= %s"
 cur.execute(comando,datos)
 data=cur.fetchall()
 cur.close()
 return render_template('editar_lote.html',parqueo=data[0])

@app.route('/update_loteparqueo/<id>' ,methods=['POST' ])
def updateloteparqueo(id):
 lote_id=id
 nombre= request.form['nombre']
 localizacion= request.form['localizacion']
 capacidad_total= request.form['capacidad_total']
 cursor =db.cursor()
 comando="UPDATE loteparqueo set nombre = %s, localizacion = %s, capacidad_total = %s where lote_id = %s"
 datos=(nombre, localizacion, capacidad_total, lote_id)
 cursor.execute(comando, datos)
 flash('Lote actualizado exitosamente')
 db.commit()
 return redirect(url_for('loteparqueo'))

@app.route('/new_loteparqueos', methods=['POST', 'GET'])
def new_loteparqueos():
 return render_template('agregar_loteparqueos.html')


@app.route('/agregar_loteparqueos',methods=['POST'])
def agregarloteparqueo():
  nombre= request.form['nombre']
  localizacion= request.form['localizacion']
  capacidad_total= request.form['capacidad_total']
  cursor =db.cursor()
  comando=" INSERT INTO loteparqueo (nombre , localizacion , capacidad_total) values (%s,%s,%s)"
  datos= (nombre, localizacion, capacidad_total)
  cursor.execute(comando,datos)
  flash('Lote agregado exitosamente')
  db.commit()
  return redirect(url_for('loteparqueo'))


@app.route('/vehiculos')
def vehiculos():
 cur=db.cursor(pymysql.cursors.DictCursor)
 cur.execute("select * from vehiculos")
 data=cur.fetchall()
 cur.close()
 return render_template('vehiculo.html',vehi=data )


@app.route('/editar_vehiculo/<id>',methods=['POST','GET'])
def editarvehiculo(id):
 cur=db.cursor(pymysql.cursors.DictCursor)
 datos=(id,)
 comando="select * from vehiculos where placa= %s"
 cur.execute(comando,datos)
 data=cur.fetchall()
 cur.close()
 return render_template('editar_vehiculo.html',vehiculo=data[0])

@app.route('/update_vehiculo' ,methods=['POST' ])
def updatevehiculo():
 placa=request.form['placa']
 cliente_id= request.form['cliente_id']
 marca= request.form['marca']
 modelo= request.form['modelo']
 tipo= request.form['tipo']
 cursor =db.cursor()
 comando="UPDATE vehiculos set cliente_id= %s, marca= %s, modelo= %s, tipo= %s where placa= %s"
 datos=(cliente_id,marca,modelo,tipo,placa)
 cursor.execute(comando, datos)
 flash('Vehiculo actualizado exitosamente')
 db.commit()
 return redirect(url_for('vehiculos'))

@app.route('/new_vehiculo', methods=['POST', 'GET'])
def new_vehiculo():
 return render_template('agregar_vehiculo.html')

@app.route('/agregar_vehiculo',methods=['POST'])
def agregarvehiculo():
  placa= request.form['placa']
  marca= request.form['marca']
  modelo= request.form['modelo']
  tipo= request.form['tipo']
  cliente_id= request.form['cliente_id']
  cursor =db.cursor()
  comando=" INSERT INTO vehiculos (cliente_id,placa,marca,modelo,tipo) values (%s,%s,%s,%s,%s)"
  datos=(cliente_id,placa,marca,modelo,tipo)
  cursor.execute(comando,datos)
  flash('Vehiculo agregado exitosamente')
  db.commit()
  return redirect(url_for('vehiculos'))



if __name__ == '__main__':
  app.run(port=3000,debug=True)