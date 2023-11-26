from flask import Flask, render_template, request, url_for, flash, redirect, abort, session
from stock_loader import StockLoader
from av_service import AlphaVantageService
from chart_service import ChartService
from datetime import datetime

HOST = "0.0.0.0"

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'your secret key'

# menu options
app.stocks = []
app.chart_types = ["Bar", "Line"]
app.time_series_types = ["Intraday", "Daily", "Weekly", "Monthly"]

app.api_key = 'J6G27DJTUEQBSYBI'
@app.before_request
def load_stock_data():
    app.stocks = StockLoader('stocks.csv').stocks

@app.route('/', methods=['GET', 'POST'])
def index():
    chart = None

    if request.method == 'POST':
        symbol = request.form['symbol']
        chart_type = request.form['chart_type']
        time_series_type = request.form['time_series_type']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        # save the form inputs to the session so we can pre-populate the form on the next request
        # if there is an error
        session['symbol'] = symbol
        session['chart_type'] = chart_type
        session['time_series_type'] = time_series_type
        session['start_date'] = start_date
        session['end_date'] = end_date
        
        if validate_inputs(symbol, chart_type, time_series_type, start_date, end_date):
            try:
                av_service = AlphaVantageService(app.api_key)
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')

                time_series = av_service.get_time_series(time_series_type, symbol, start_date, end_date)
                chart_service = ChartService()
                chart = chart_service.create_chart(chart_type, time_series)

                # clear the session on success
                session.clear()
            except Exception as e:
                flash(str(e))
                return redirect(url_for('index'))

    return render_template('index.html', stocks=app.stocks, chart_types=app.chart_types, time_series_types=app.time_series_types, chart=chart)

def validate_inputs(symbol, chart_type, time_series_type, start_date, end_date) -> bool:
    valid = True

    # symbol exists and is valid (in the list of stocks)
    if not symbol or symbol not in [stock.symbol for stock in app.stocks]:
        flash('Symbol is required!')
        valid = False
    # chart type exists and is valid
    if not chart_type or chart_type not in app.chart_types:
        flash('Chart Type is required!')
        valid = False
    # time series exists and is valid
    if not time_series_type or time_series_type not in app.time_series_types:
        flash('Time Series is required!')
        valid = False
    # start date and end date exists
    if not start_date or not end_date:
        flash('Start and End Date are required!')
        valid = False
    else:
        # we have dates, so we can do extra validation.
        # validate that date strings are in the correct format of YYYY-MM-DD
        try:
            start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
        except ValueError:
            flash('Start Date must be in the format YYYY-MM-DD!')
            valid = False
        try:
            end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            flash('End Date must be in the format YYYY-MM-DD!')
            valid = False
        # validate that start date is before end date
        if start_datetime > end_datetime:
            flash('End Date must be greater than or equal to Start Date!')
            valid = False
        # validate that intraday time series is not more than 30 days
        if time_series_type == 'Intraday' and (end_datetime - start_datetime).days > 30:
            flash('Due to a limitation of the AlphaVantage API, Intraday time series cannot be more than 30 days!')
            valid = False
    
    return valid


# start the flask app
app.run(host=HOST)