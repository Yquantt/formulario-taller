from flask import Flask, request, redirect, render_template
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Conexión a Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("taller-service-account.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Registro Taller").sheet1  # Usa el nombre exacto de tu hoja

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

    # Agregar fila a Google Sheets
    fila = list(datos.values())
    sheet.append_row(fila)

    return redirect('/')

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

