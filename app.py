from flask import Flask, render_template, request
from waitress import serve
from io import BytesIO
from bs4 import BeautifulSoup
import requests
from flask import Response, make_response
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('Agg')
keys_removed = (' ', '_', '\n', '-', "'", '©', '"', '%')
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('form.html');
 
@app.route('/data/', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        global url
        form_data = request.form
        url = form_data.get('Name')

    return render_template('data.html',form_data = form_data)

@app.route('/plot.png')
def plotting():
    img = BytesIO()
    chars = {}
    print("URL2:", url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    for i in soup.get_text():
        if i in chars:
            chars[i] += 1 

        else:
            chars[i] = 1
    for x in keys_removed:
        chars.pop(x, None)

    plt.figure()
    graphChars = sorted(chars.items(), key=lambda kv: (kv[1], kv[0]))
    graphChars = graphChars[-10::1]
    print("chars:", graphChars)
    x, y = zip(*graphChars)

    plt.title("Character Amount on Page", fontsize = 20)
    plt.xlabel("Character", fontsize=14)
    plt.ylabel("Occured", fontsize=14)
    plt.plot(x, y)
    plt.savefig(img, format='png')
    img.seek(0)

    response=make_response(img.getvalue())
    response.headers['Content-Type'] = 'image/png'
    img.close()
    return response

if __name__ == '__main__':
    # serve(app, host='0.0.0.0', port=4206)
    app.run(debug = True)