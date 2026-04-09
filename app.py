from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/calcular', methods=['GET', 'POST'])
def calcular():
    imc = None
    clasificacion = ""
    recomendacion = ""

    if request.method == 'POST':
        peso = float(request.form['peso'])
        estatura = float(request.form['estatura'])

        imc = round(peso / (estatura ** 2), 2)

        # Clasificación OMS
        if imc < 18.5:
            clasificacion = "Bajo peso"
            recomendacion = "Se recomienda mejorar la alimentación y consultar un especialista."

        elif 18.5 <= imc < 25:
            clasificacion = "Peso normal"
            recomendacion = "¡Buen trabajo! Mantén una dieta equilibrada y ejercicio regular."

        elif 25 <= imc < 30:
            clasificacion = "Sobrepeso"
            recomendacion = "Se recomienda realizar actividad física y mejorar hábitos alimenticios."

        else:
            clasificacion = "Obesidad"
            recomendacion = "Es importante consultar a un profesional de la salud."

    return render_template('calculadora.html',
                           imc=imc,
                           clasificacion=clasificacion,
                           recomendacion=recomendacion)

@app.route("/contacto")
def contacto():
    return render_template("contacto.html")

if __name__ == "__main__":
    app.run(debug=True)
