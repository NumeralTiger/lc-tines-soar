import os, json
from flask import Flask, request, jsonify
from limacharlie_client import isolate_sensor, get_sensor_info
from notifier import send_slack_alert, send_email

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "LimaCharlie <-> Tines SOAR demo webhook. POST /detect to simulate."

@app.route("/detect", methods=["POST"])
def detect():
    """
    Main webhook endpoint that accepts detection payloads. Example payload:
    {
      "event":"suspicious_process",
      "sid":"SENSOR_ID_HERE",
      "host":"host.example.com",
      "evidence":"process X downloaded exe",
      "severity":"high"
    }
    """
    data = request.get_json(force=True)
    sid = data.get("sid")
    host = data.get("host","unknown")
    severity = data.get("severity","medium")
    event = data.get("event","detection")
    evidence = data.get("evidence","n/a")

    # 1) Notify analysts (Slack + Email)
    text = f"*Detection*: {event}\n*Host*: {host}\n*SID*: {sid}\n*Severity*: {severity}\n*Evidence*: {evidence}"
    try:
        send_slack_alert(text)
    except Exception as e:
        app.logger.exception("Slack notify failed: %s", e)

    try:
        send_email(f"[ALERT] {event} on {host}", text)
    except Exception as e:
        app.logger.exception("Email notify failed: %s", e)

    # 2) Automated containment policy: if severity is high => isolate
    auto_isolate = severity.lower() == "high"
    resp = {"notified": True, "auto_isolate": auto_isolate}
    if auto_isolate and sid:
        try:
            iso = isolate_sensor(sid, reason=f"Auto isolation for event {event}")
            resp["isolation_result"] = iso
            send_slack_alert(f"Isolation executed for {host} (SID: {sid}).")
        except Exception as e:
            app.logger.exception("Isolation failed: %s", e)
            resp["isolation_error"] = str(e)

    return jsonify(resp), 200

if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 5000))
    app.run(host="0.0.0.0", port=port)
