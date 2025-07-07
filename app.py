
from flask import Flask, request, redirect, render_template
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)
ARCHIVO_EXCEL = "registro_taller.xlsx"

@app.route('/')
def index():
    return render_template('formulario.html')

@app.route('/guardar', methods=['POST'])
def guardar():
    datos = {
        "Fecha": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "Marca y Modelo": request.form['modelo'],
        "Patente": request.form['patente'],
        "Año": request.form['anio'],
        "Color": request.form['color'],
        "Kilometraje": request.form['km'],
        "Checklist": ", ".join(request.form.getlist('checklist')),
        "Observaciones": request.form['observaciones'],
        "Mecanico": request.form['mecanico']
    }

    if os.path.exists(ARCHIVO_EXCEL):
        df = pd.read_excel(ARCHIVO_EXCEL)
        df = pd.concat([df, pd.DataFrame([datos])], ignore_index=True)
    else:
        df = pd.DataFrame([datos])

    df.to_excel(ARCHIVO_EXCEL, index=False)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
