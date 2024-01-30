from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_mysqldb import MySQL
app = Flask(__name__)


@app.before_request
def before_request():
    print("Antes de la petición...")


@app.after_request
def after_request(response):
    print("Después de la petición")
    return response


@app.route('/')
def index():
    cursos = ['PHP','Python','Java','Kotlin','Dart','JavaScript']
    data = {
        'titulo': 'Index',
        'bienvenida': '¡Saludos!',
        'cursos':cursos,
        'numero_cursos':len(cursos)
    }
    return render_template('index.html', data=data)



@app.route('/contacto/<nombre>/<int:edad>')
def contacto(nombre, edad):
    data = {
        'titulo': 'Contacto',
        'nombre': nombre,
        'edad': edad
    }
    return render_template('contacto.html', data=data)

def query_string():
    print(request)
    print(request.args)
    print(request.args.get('param1'))
    print(request.args.get('param2'))
    return "Ok"


@app.route('/cursos')
def listar_cursos():
    data = {}
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT codigo, nombre, creditos FROM curso ORDER BY nombre ASC"
        cursor.execute(sql)
        cursos = cursor.fetchall()
        # print(cursos)
        data['cursos'] = cursos
        data['mensaje'] = 'Exito'
    except Exception as ex:
        data['mensaje'] = 'Error...'
    return jsonify(data)



@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'GET':
        return render_template('registro.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validar que los campos no estén vacíos
        if not username or not password:
            return render_template('registro.html', error='Los campos no pueden estar vacíos')

        # Guardar el usuario en la base de datos
        from app.models import User

        user = User(username=username, password=password)
        user.save()

        return redirect(url_for('index'))


def pagina_no_encontrada(error):
    #return render_template('404.html'), 404
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.add_url_rule('/query_string', view_func=query_string)
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True, port=5000)
