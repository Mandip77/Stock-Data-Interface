import pandas as pd
import requests
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        symbol = request.form.get('symbol')
        request.form.get('start')
        request.form.get('end')
        data_type = request.form.get('data_type')

        function_map = {
            "Monthly": "TIME_SERIES_MONTHLY_ADJUSTED",
            "Weekly": "TIME_SERIES_WEEKLY_ADJUSTED",
            "Daily": "TIME_SERIES_DAILY_ADJUSTED"
        }

        url = "https://alpha-vantage.p.rapidapi.com/query"
        querystring = {
            "symbol": symbol,
            "function": function_map[data_type],
            "datatype": "json"
        }

        headers = {
            "X-RapidAPI-Key": "019e03847dmsh111ec23d59afa58p185f5assn8ce8f1d08169",
            "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code != 200:
            return render_template('error.html')

        else:
            data = response.json()
            time_series_data = data[f"{data_type} Adjusted Time Series"]
            df = pd.DataFrame.from_dict(time_series_data, orient="index")
            df.index = pd.to_datetime(df.index)
            df = df.astype(float)

            return render_template('data.html', tables=[df.to_html(classes='data')], titles=df.columns.values)

    else:
        return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
