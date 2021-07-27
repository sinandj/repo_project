from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL, MySQLdb
import bcrypt

app = Flask(__name__)

# Conexión Mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1q2w3e4r'
app.config['MYSQL_DB'] = 'agendamiento'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

# Direccionamiento al home
@app.route('/')
def home():
    return render_template('home.html')

# Registro de nuevo usuario en bases de datos
@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        documento = request.form['documento']
        fecha_nac = request.form['fecha_nac']
        celular = request.form['celular']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO usuarios (documento, nombre, apellido, fecha_nac, email, celular, password) VALUES (%s, %s, %s, %s, %s, %s, %s)', (documento, nombre, apellido, fecha_nac, email, celular, hash_password))
        mysql.connection.commit()
        session['nombre'] = nombre
        session['email'] = email
        return redirect(url_for("home"))

# Logueo
@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM usuarios WHERE email=%s",(email,))
        user = cur.fetchone()
        cur.close()

        if len(user) > 0:
            if bcrypt.hashpw(password, user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
                session['nombre'] = user['nombre']
                session['email'] = user['email']
                return render_template("home.html")
            else:
                return "Usuario o contraseña incorrecta"
        else:
            return "Usuario o contraseña incorrecta"
    else:
        return render_template("login.html")

# Confirmación de citas medicas
@app.route('/confirm', methods=["GET","POST"])
def confirm():
    if request.method == 'GET':
        return render_template("confirm.html")
    else:
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        celular = request.form['celular']
        email = request.form['email']
        fecha_cita = request.form['fecha_cita']
        hora_cita = request.form['hora_cita']
        area = request.form['area']
        doctor = request.form['doctor']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO citas (nombre, apellido, celular, email, fecha_cita, hora_cita, area, doctor) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (nombre, apellido, celular, email, fecha_cita, hora_cita, area, doctor))
        mysql.connection.commit()
        #session['nombre'] = nombre
        #session['email'] = email
        return redirect(url_for("home"))

# Redireccionamiento a otras secciones
@app.route('/department')
def department():
    return render_template('department.html')

@app.route('/doctors')
def doctors():
    return render_template('doctors.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# Salida del portal
@app.route('/logout')
def logout():
    session.clear()
    return render_template("home.html")


if __name__ == '__main__':
    app.secret_key = 'Ao!UQf)2qK3h#04' #mysecretkey
    app.run(port=3000, debug=True)