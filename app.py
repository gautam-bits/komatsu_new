from flask import Flask, render_template, request
import json

app = Flask(__name__)


def data_fetch(fname):
    with open(fname, 'r') as f:
        data = json.load(f)
    
    return data

def data_fetch_byorder(fname, id):
    data2 = data_fetch(fname)
    for i in data2['page2data']:
        if i["job_id"] == int(id):
            return i

@app.route("/", methods=["GET", "POST"])
def hello():
    if request.method == "POST":
        id = request.form['id']
        up_data = {
            "order_id": id,
            "status": "confirmed"
        }
        print(up_data)
    
    color = {
        "color": {
            'Recieved': '#228B22',
            'Stopped': '#D22B2B',
            'Restarting': '#F28C28',
            'Picking': '#00008B', 
            'Waiting': '#ADD8E6'
        }
    }

    data = data_fetch('homepage_api_data.json')
    data.update(color)

    return render_template('home.html', data=data)


@app.route('/2/<order_id>')
def tw(order_id):
    data = data_fetch_byorder('page2_api_data.json', order_id)
    return render_template('2.html', data=data)

@app.route('/7')
def sev():
    return render_template('7.html')

@app.route('/10')
def ten():
    return render_template('10.html')

@app.route('/18')
def eighteen():
    return render_template('18.html')

@app.route('/19')
def nin():
    return render_template('19.html')


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(port=1000)