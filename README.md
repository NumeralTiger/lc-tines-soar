# LimaCharlie + Tines Automated Incident Response Demo

This repository demonstrates an automated incident response pipeline that integrates **LimaCharlie (EDR)** and **Tines (SOAR)** to detect and contain simulated endpoint threats in real-time.

It includes:

* A Flask-based webhook service for detection intake and orchestration.
* Integration with the LimaCharlie API to isolate (contain) endpoints automatically.
* Slack and email alerting for rapid analyst response.
* Example Tines' story for orchestrating end-to-end detection and containment.

---

## 🧩 Architecture Overview

```
[Sensor / Endpoint] --> LimaCharlie (EDR)
 |
 v
 [Tines (SOAR)] ---> (HTTP Request) ---> [Flask Orchestration Service]
 |                                         |
 |                                         v
 |                                  LimaCharlie API (POST /{sid}/isolation)
 |
 +--> Slack (alerts) & Email (notifications)
```

**Flow Summary:**

1. A detection event is generated from LimaCharlie or a simulated endpoint.
2. Tines receives the event and triggers the Flask webhook service.
3. The Flask service alerts analysts via Slack and email.
4. If the severity is *high*, the endpoint is automatically isolated via LimaCharlie.
5. Tines logs the action, and Slack alerts confirm containment.

---

## ⚙️ Setup Instructions

### 1. Prerequisites

* [Python 3.8+](https://www.python.org/downloads/)
* [LimaCharlie Account](https://app.limacharlie.io)
* [Tines Account](https://www.tines.com/)
* Slack workspace with an [Incoming Webhook](https://api.slack.com/messaging/webhooks)

### 2. Clone the Repository

```bash
git clone https://github.com/<your-username>/lc-tines-soar.git
cd lc-tines-soar
```

### 3. Set Up Environment Variables

Copy the sample configuration and fill in your credentials:

```bash
cp app/config.example.env .env
```

Edit `.env` with your credentials:

```ini
LIMACHARLIE_API_KEY=your_api_key_here
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXXX/XXXX/XXXX
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=alert@example.com
SMTP_PASSWORD=your_password
ALERT_TO_EMAIL=soc_team@example.com
```

### 4. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Run the Webhook Service

```bash
FLASK_APP=app/app.py flask run --host=0.0.0.0 --port=5000
```

The service will start listening at `http://localhost:5000`.

---

## 🧪 Testing the Pipeline

### Simulate a Detection Event

```bash
curl -X POST -H "Content-Type: application/json" \
 --data @examples/sample_detection.json \
  http://localhost:5000/detect
```

**Expected behaviour:**

* Slack alert and email notification sent.
* Endpoint automatically isolated (if `severity` is `high`).
* JSON response confirms status and isolation results.

---

## 🧠 Using with Tines

### Create a Tines Story

1. Create a **Webhook Action** in Tines to receive events (or forward detections from LimaCharlie).
2. Add an **Event Transformation Action** to parse JSON fields (`sid`, `severity`, etc.).
3. Add a **Conditional Action**:

   * If `severity == high`, use an **HTTP Request Action** to call:

 ```
 POST https://api.limacharlie.io/v1/{{sid}}/isolation
 Headers: Authorization: Bearer <LIMACHARLIE_API_KEY>
 Body: {"reason": "Automated containment via Tines"}
 ```
4. Add a **Slack Action** or **HTTP Request Action** to send notifications.

### Import Example Story

An example Tines story (`examples/tines_story.md`) is provided to help you recreate the flow.

---

## 🔒 Security Notes

* **Do not** commit API keys or secrets to GitHub.
* Use `.env` or a secret manager (e.g., AWS Secrets Manager, Vault).
* LimaCharlie API calls require a scoped API key with isolation permissions.
* Secure webhook endpoints with authentication or IP whitelisting.

---

## 📬 Notifications

The project includes:

* **Slack Notifications:** Sent via Incoming Webhook.
* **Email Alerts:** Sent via SMTP for high-severity detections.

Both can be customized in `app/notifier.py`.

---

## 📄 References

* [LimaCharlie REST API Documentation](https://doc.limacharlie.io/docs/api-reference)
* [Tines Webhook & HTTP Request Actions](https://www.tines.com/docs/actions/webhook)
* [Slack Incoming Webhooks](https://api.slack.com/messaging/webhooks)
* [Python Flask Documentation](https://flask.palletsprojects.com/)

---