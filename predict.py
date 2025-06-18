from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__, template_folder='templates', static_folder='template/assets')

model = pickle.load(open('./models/pipe.pkl', 'rb'))

@app.route('/')
def home():
    return render_template("homepage.html")

@app.route('/dados_imovel')
def dados_imovel():
    return render_template("form.html")

def get_data():
    longitude = float(request.form.get('longitude'))
    latitude = float(request.form.get('latitude'))
    housing_median_age = float(request.form.get('housing_median_age'))
    total_rooms = float(request.form.get('total_rooms'))
    total_bedrooms = float(request.form.get('total_bedrooms'))
    population = float(request.form.get('population'))
    households = float(request.form.get('households'))
    median_income = float(request.form.get('median_income'))
    ocean_proximity = request.form.get('ocean_proximity')
    rooms_per_household = float(request.form.get('rooms_per_household'))
    bedrooms_per_room = float(request.form.get('bedrooms_per_room'))

    data = {
        'longitude': [longitude],
        'latitude': [latitude],
        'housing_median_age': [housing_median_age],
        'total_rooms': [total_rooms],
        'total_bedrooms': [total_bedrooms],
        'population': [population],
        'households': [households],
        'median_income': [median_income],
        'ocean_proximity': [ocean_proximity],
        'rooms_per_household': [rooms_per_household],
        'bedrooms_per_room': [bedrooms_per_room]
    }

    return pd.DataFrame(data)

@app.route('/send', methods=['POST'])
def predict():
    df = get_data()
    prediction = model.predict(df)
    resultado = f'O valor estimado do imóvel é ${prediction[0]:,.2f}'

    return render_template("result.html", resultado=resultado, tabela=df.to_html(classes='data'))

if __name__ == "__main__":
    app.run(debug=True)
