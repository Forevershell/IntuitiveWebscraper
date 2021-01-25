from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import threading
import intuitive_webscraper.process_stocks as process
from intuitive_webscraper.parse_tickers import getTickers

app = Flask(__name__)

# Index Route / App Main Page
@app.route('/', methods=['POST', 'GET'])
def index():
    # If a new stock (based on symbol) is requested
    if request.method == 'POST':
        ticker = request.form['ticker']
        try:
            stock = process.getStock(ticker)
            return redirect('/')
        except Exception as inst:
            return redirect('/error/' + str(inst))
    # Normal index page, viewing all saved stocks
    else:
        stocks = process.getStocks()
        return render_template('index.html', stocks=stocks)

# Deleting a saved stock by removing the cache
@app.route('/delete/<string:name>')
def delete(name):
    try:
        process.removeStock(name)
        return redirect('/')
    except:
        return 'Problem deleting stock'

# Error Page (Stock not found, etc.)
@app.route('/error/<string:error>')
def notFound(error):
    return render_template('error.html', error = error)

# Viewing all the exchanges to navigate through stock exchange
@app.route('/stocks')
def listStocks():
    try:
        exchanges = process.getExchanges()
        return render_template('exchanges.html', exchanges=exchanges)
    except:
        return render_template('loading.html')

# Viewing all the stocks in each exchange
@app.route('/stocks/<string:name>')
def listExchange(name):
    try:
        tickers = process.getTickersInExchange(name)
        return render_template('ticker.html', tickers=tickers, exchange = name)
    except:
        return render_template('loading.html')

# Adding specific stock to the watchlist
@app.route('/stocks/<string:exchange>/<string:ticker>')
def addToWatchlist(exchange, ticker):
    try:
        stock = process.getStock(ticker)
        return redirect('/')
    except Exception as inst:
        return redirect('/error/' + str(inst))

# Shutting down the server
@app.route('/shutdown', methods=['GET', 'POST'])
def shutdown():
    request.environ.get('werkzeug.server.shutdown')()
    return render_template('bye.html') 

if __name__ == "__main__":
    # Start updating tickers
    threading.Thread(target=getTickers).start()
    app.run(debug=False, use_reloader=False, threaded = False)