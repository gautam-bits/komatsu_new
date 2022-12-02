from flask import Flask, render_template, request
import json
from flask_qrcode import QRcode


# Status translations
# Recieved: 受取済み same as picking done / done   / approval completed
# Stopped: 停止中  restart / 
# Picking: 移動中 stop
# Waiting: 待機中 stop
# Restarting: 再開中 stop
# send robot id as a response too in getrobot
# barcode


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
    with open(fname, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data

def dump_data(fname, data):
    with open(fname, "w", encoding='utf-8') as outfile:
        json.dump(data, outfile)

def data_fetch_byorder(fname, id):
    data2 = data_fetch(fname)
    for i in data2['jobs']:
        if i == id:
            return data2['jobs'][i]

@app.route("/", methods=["GET", "POST"])
def hello():
    if request.method == "POST":
        id = request.form['id']
        up_data = {
            "order_id": id,
            "status": "confirmed"
        }
        print(up_data)

    data2 = data_fetch('current_orders.json')
    hmpgata = []
    count = 1
    for itemid in data2["jobs"]:
        item = data2["jobs"][itemid]
        hmpgata.append(
            {"serial_number": count,
            "name": item["job_details"]["ref_num"],
            "order_id": item["job_id"],
            "status": item["status"]
        })
        count+=1
    data = {
        "homepageData": hmpgata
    }
    data.update(color)

    return render_template('home.html', data=data)

@app.route("/getjob/robot/<robot_num>", methods=["GET"])
def getjob(robot_num):
    data = data_fetch('current_orders.json')
    
    jobid = data['jobs_waiting'].pop(0)
    data['jobs'][jobid]['status'] = "Picking"
    data['jobs'][jobid]['robot_id'] = robot_num

    job = data['jobs'][jobid]
    dump_data('current_orders.json', data)

    data = data_fetch('robot_temp_db.json')
    data[robot_num]["job_id"]=job["job_id"]
    data[robot_num]["status"]="Picking"
    dump_data('robot_temp_db.json', data)
    return job

@app.route("/job-status/robot/<robot_num>", methods=["GET", "POST"])
def jobstat(robot_num):
    data = data_fetch('robot_temp_db.json')
    data2 = data_fetch('current_orders.json')
    if request.method == "POST":
        # expecting {"status": "newstatus"}
        req = request.json
        newstatus = req.get("status")
        if newstatus is None:
            newstatus = "Unspecified"
        data[robot_num]["status"] = newstatus
        data2['jobs'][data[robot_num]["job_id"]]["status"]= newstatus
        dump_data('robot_temp_db.json', data)
        dump_data('current_orders.json', data2)
        return data[robot_num]
    else:
        return data[robot_num]



@app.route("/robotlist", methods=["GET"])
def robotlist():

    data = data_fetch('robot_temp_db.json')

    data_list = []

    for el in data.keys():
        data_list.append(data[el])
    
    robot_list_data = {
        "robot_list_data": data_list
    }

    return render_template('robot.html', data=robot_list_data)

@app.route("/pastorders", methods=["GET"])
def pastorders():

    data2 = data_fetch('pastorders_api_data.json')
    hmpgata = []
    count = 1
    for itemid in data2["jobs_completed"]:
        item = data2["jobs_completed"][itemid]
        hmpgata.append(
            {"serial_number": count,
            "name": item["job_details"]["ref_num"],
            "order_id": item["job_id"],
            "status": item["status"]
        })
        count+=1
    data = {
        "homepageData": hmpgata
    }
    data.update(color)

    return render_template('pastorders.html', data=data)


@app.route('/2/<order_id>')
def tw(order_id):
    data = data_fetch_byorder('current_orders.json', order_id)
    print(data)
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