from flask import Flask, render_template
import json

app = Flask(__name__)


def home_data():
    with open('homepage_api_data.json', 'r') as f:
        data = json.load(f)
    
    return data


@app.route("/")
def hello():
    # f = open('data.json')
    # data = {
    #         "job_id": 155212,
    #         "robot_num": 1,
    #         "job_details": {
    #             "box_num": 221,
    #             "ref_num": "DX87824239",
    #             "location": "D2",
    #             "part_num": 39,
    #             "item": "screw",
    #             "position": [125, 874, 985]
    #         }
    #      }

    color = {
        "color": {
            'Recieved': '#228B22',
            'Stopped': '#D22B2B',
            'Restarting': '#F28C28',
            'Picking': '#00008B', 
            'Waiting': '#ADD8E6'
        }
    }

    data = home_data()
    data.update(color)
    print(data)

    return render_template('home.html', data=data)


@app.route('/2')
def tw():
    return render_template('2.html')

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