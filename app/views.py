from flask import render_template, request, redirect, url_for
from app import app
import csv

ficherotransacciones = "data/transacciones.dat"
fields = ['fecha', 'hora', 'descripcion', 'monedaComprada', 'cantidadComprada', 'monedaPagada', 'cantidadPagada']

@app.route('/')
def index():
    transacciones = open(ficherotransacciones, 'r')
    csvreader = csv.reader(transacciones, delimiter=',', quotechar='"' )

    movimientos = []
    for campos in csvreader:
        camposdict = {}
        for ix, field in enumerate(fields):
            camposdict[field] = campos[ix]
        '''
        camposdict = {
            'fecha': campos[0],
            'hora': campos[1],
            'descripcion': campos[2],
            'monedaComprada': campos[3],
            'cantidadComprada': campos[4],
            'monedaPagada': campos[5],
            'cantidadPagada': campos[6],
        }
        '''
        movimientos.append(camposdict)

    return render_template('index.html', movimientos=movimientos)

@app.route('/nuevacompra', methods=['GET', 'POST'])
def nuevacompra():
    if request.method == 'GET':
        if request.values['btnselected'] == 'Nueva':
            return render_template('nuevacompra.html')
        else:
            ix = int(request.values['ix'])
            transacciones = open(ficherotransacciones, 'r')
            csvreader = csv.reader(transacciones, delimiter=',', quotechar='"' )
            for numreg, registro in enumerate(csvreader):
                if numreg == ix:
                    camposdict = {}
                    for ix, field in enumerate(fields):
                        camposdict[field] = registro[ix]

                    return render_template('modificacompra.html', registro=camposdict)
            return 'Movimiento no encontrado'
    else:
        datos = request.form
        transacciones = open(ficherotransacciones, "a+")
        registro = '{},{},"{}",{},{},{},{}\n'.format(request.form['fecha'],request.form['hora'],request.form['descripcion'],request.form['monedaComprada'],request.form['cantidadComprada'],request.form['monedaPagada'],request.form['cantidadPagada'])
        
        transacciones.write(registro)
        transacciones.close()
        return redirect(url_for('index'))
