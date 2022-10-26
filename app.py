from flask import Flask, render_template
import json

app = Flask(__name__)


if __name__ == '__main__':
    app.run(port=1000)

@app.route('/')
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
    #     }
    return render_template('home.html')


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
