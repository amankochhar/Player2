# importing all the modules for the apps
import scripts
from flask import Flask, render_template, request

app = Flask(__name__)
# False for production code
app.debug = True

# handles each link called from the website
# default index page
@app.route("/")
def index():
    staticJSON = scripts.dash.index()
    return render_template('layouts/index.html', staticJSON=staticJSON)

# fir the custom queries from the page
@app.route('/_custom/') 
def custom():
    query = request.args.get('query', "Null", type=str)
    X = request.args.get('X', "Null", type=str)
    Y = request.args.get('Y', "Null", type=str)
    customPlot = scripts.dash.custom(query, X, Y)
    return customPlot

# this is where the pubsub topic should push messages to
@app.route('/_pubsub/')
def processMessage():
    data = request.args.get('data', "Null", type=str)
    # this handles messages for both the raw and the processed table in bigquery
    scripts.pubsub.post(data)
    return

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
