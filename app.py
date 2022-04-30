# Importing the libraries needed
from flask import Flask, render_template, request, Response, make_response
from waitress import serve
from io import BytesIO
from bs4 import BeautifulSoup
import requests
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('Agg') # This allows matplotlib work outside the mainthread


# Globally initializing the characters that will not show
global keys_removed
keys_removed = (' ', '_', '\n', '-', "'", '©', '"', '%')

app = Flask(__name__) # Creating an instance of flask 

@app.route("/") # Landing page that asks for URL
def hello():
    return render_template('form.html');

# Grabs data from form and outputs to the user
@app.route('/data/', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET': # If the page is refreshed it renders form.html, otherwise grabs the url and renders data.html
        return render_template('form.html')
    if request.method == 'POST':
        global url
        form_data = request.form
        url = form_data.get('URL')
    return render_template('data.html',form_data = form_data)

@app.route('/extra/', methods = ['GET']) # Called when ALL DATA button is clicked and gets all data if user is curious not sorted
def extra():
    return render_template('extra.html', chars = chars)

@app.route('/plot.png')
def plotting():
    # Creating global variable so it can be used across different scopes and initializing variables
    global chars
    img = BytesIO()
    chars = {}
    
    # Sending request to get all text from URL with the html.parser
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    
    # Runs through all characters and counts
    for i in soup.get_text(): 
        if i in chars:
            chars[i] += 1

        else:
            chars[i] = 1
    for x in keys_removed:
        chars.pop(x, None)

    plt.figure() # Creating a figure that will be shown to the user

    # Sorting items and using lambda to place information ex. ('A', 5) then splicing for the top ten and adding the data with zip()
    graphChars = sorted(chars.items(), key=lambda kv: (kv[1], kv[0]))
    graphChars = graphChars[-10::1]
    x, y = zip(*graphChars)

    # Giving labels to the table
    plt.title("Character Amount on Page", fontsize = 20)
    plt.xlabel("Character", fontsize=14)
    plt.ylabel("Occured", fontsize=14)
    plt.plot(x, y)

    # Saving the created figure into a png format so it can be displayed to the user
    plt.savefig(img, format='png')
    img.seek(0)
    response=make_response(img.getvalue())
    response.headers['Content-Type'] = 'image/png'
    img.close()

    return response # Returns the PNG of the graphed data


# main
if __name__ == '__main__':
    # serve(app, host='0.0.0.0', port=4206)
    app.run(debug = True)