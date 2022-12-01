from flask import Flask, render_template, request
import json
from flask_qrcode import QRcode


# Status translations
# Recieved: 受取済み
# Stopped: 停止中
# Picking: 移動中
# Waiting: 待機中
# Restarting: 再開中


# GLOBAL CONST:
color = {
        "color": {
            '受取済み': '#42d935',
            '停止中': '#fb0724',
            '再開中': '#fc6f08',
            '移動中': '#0914f7', 
            '待機中': '#0f75ed'
        }
    }


app = Flask(__name__)
QRcode(app)


def data_fetch(fname):
    with open(fname, 'r') as f:
        data = json.load(f)
    
    return data

def dump_data(fname, data):
    with open(fname, "w") as outfile:
        json.dump(data, outfile)

def data_fetch_byorder(fname, id):
    data2 = data_fetch(fname)
    for i in data2['page2data']:
        if i["job_id"] == id:
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

    data = data_fetch('homepage_api_data.json')
    data.update(color)

    return render_template('home.html', data=data)

@app.route("/getjob/robot/<robot_num>", methods=["GET"])
def getjob(robot_num):
    data = data_fetch('current_orders.json')
    
    job = data['jobs_queue'].pop(0)
    data['jobs_completed'].append(job)
    dump_data('current_orders.json', data)

    data = data_fetch('robot_temp_db.json')
    data[robot_num]["job_id"]=job["job_id"]
    data[robot_num]["status"]="Picking"
    dump_data('robot_temp_db.json', data)
    return job

@app.route("/job-status/robot/<robot_num>", methods=["GET", "POST"])
def jobstat(robot_num):
    data = data_fetch('robot_temp_db.json')
    if request.method == "POST":
        # expecting {"status": "newstatus"}
        req = request.json
        newstatus = req.get("status")
        if newstatus is None:
            newstatus = "Unspecified"
        data[robot_num]["status"] = newstatus
        dump_data('robot_temp_db.json', data)
        return data[robot_num]
    else:
        return data[robot_num]



@app.route("/robotlist", methods=["GET"])
def robotlist():

    data = data_fetch('robot_api_data.json')

    return render_template('robot.html', data=data)

@app.route("/pastorders", methods=["GET"])
def pastorders():

    data = data_fetch('pastorders_api_data.json')
    data.update(color)

    return render_template('pastorders.html', data=data)


@app.route('/2/<order_id>')
def tw(order_id):
    data = data_fetch_byorder('page2_api_data.json', order_id)
    return render_template('2.html', data=data)

@app.route('/7')
def sev():
    return render_template('7.html')

@app.route('/10')
def ten():
    data = data_fetch('homepage_api_data.json')
    data.update(color)
    data.update(data_fetch('page10_api_data.json'))

    return render_template('10.html', data=data)

@app.route('/18')
def eighteen():
    return render_template('18.html')

@app.route('/19')
def nin():
    return render_template('19.html')


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(port=1000)