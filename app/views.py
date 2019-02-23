from flask import render_template, request, redirect, url_for
from app import app
import csv
import os

ficherotransacciones = "data/transacciones.dat"
nuevoficherotransacciones = 'data/newtransacciones.dat'

fields = ['fecha', 'hora', 'descripcion', 'monedaComprada', 'cantidadComprada', 'monedaPagada', 'cantidadPagada']

def makeDict(lista):
    diccionario = {}
    for ix, field in enumerate(fields):
        diccionario[field] = lista[ix]
    return diccionario

def makeReg(form):
    return '{},{},"{}",{},{},{},{}\n'.format(form['fecha'],form['hora'],form['descripcion'],form['monedaComprada'],form['cantidadComprada'],form['monedaPagada'],form['cantidadPagada'])

@app.route('/')
def index():
    transacciones = open(ficherotransacciones, 'r')
    csvreader = csv.reader(transacciones, delimiter=',', quotechar='"' )

    movimientos = []
    for campos in csvreader:
        camposdict = makeDict(campos)
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
        if len(request.values) == 0 or request.values.get('btnselected') == 'Nueva':
            return render_template('nuevacompra.html')
        elif request.values.get('btnselected')=='Borrar':
            if request.values.get('ix')!=None:
                registroseleccionado=int(request.values.get('ix'))
                transacciones = open(ficherotransacciones, 'r')
                newtransacciones = open(nuevoficherotransacciones, 'w+')    
                registroseleccionado = int(request.values.get('ix'))

                archivo = transacciones.readlines()
                transacciones.seek(0)
                numreg=0
                for linea in archivo:
                    if numreg != registroseleccionado:
                        newtransacciones.write(linea)
                    numreg += 1
                   
                transacciones.close()
                newtransacciones.close()
                os.remove(ficherotransacciones)
                os.rename(nuevoficherotransacciones, ficherotransacciones)

                return redirect(url_for('index'))

            else:
                return redirect(url_for('index'))

        else:
            if request.values.get('ix') != None:
                registroseleccionado = int(request.values.get('ix'))
                transacciones = open(ficherotransacciones, 'r')
                csvreader = csv.reader(transacciones, delimiter=',', quotechar='"' )
                
                for numreg, registro in enumerate(csvreader):
                    if numreg == registroseleccionado:
                        camposdict = makeDict(registro)
                        camposdict['registroseleccionado'] = registroseleccionado
                        return render_template('modificacompra.html', registro=camposdict)
                return 'Movimiento no encontrado'
                
            else:
                return redirect(url_for('index'))

    else:
        datos = request.form
        transacciones = open(ficherotransacciones, "a+")
        registro = makeReg(request.form)
        
        transacciones.write(registro)
        transacciones.close()
        return redirect(url_for('index'))

@app.route('/modificacompra', methods=['POST'])
def modificacompra():
    
    transacciones = open(ficherotransacciones, 'r')
    newtransacciones = open(nuevoficherotransacciones, 'w+')
    
    registroseleccionado = int(request.form['registroseleccionado'])

    linea = transacciones.readline()
    numreg = 0
    while linea != "":
        if numreg == registroseleccionado:
            linea = makeReg(request.form)

        newtransacciones.write(linea)
        linea = transacciones.readline()
        numreg += 1

    transacciones.close()
    newtransacciones.close()
    os.remove(ficherotransacciones)
    os.rename(nuevoficherotransacciones, ficherotransacciones)

    return redirect(url_for('index'))

    
