Title: LimaCharlie detection -> Tines orchestration -> containment + alert

Overview:
1) Webhook Action: receives detection events from sensors (or other tools). Configure to accept JSON.
   - Example incoming JSON: examples/sample_detection.json

2) Event Transformation Action: parse payload, extract sid, host, severity, evidence

3) Conditional Action:
   - If severity == "high":
       -> HTTP Request Action: POST to your Flask webhook /detect (or directly call LimaCharlie isolation endpoint)
         - URL: https://<your-host>/detect
         - Body: raw JSON of original detection
       -> Slack Action / Incoming Webhook: send alert message
       -> (Optional) Create ticket in ticketing system
   - Else:
       -> Create low-priority ticket / email to SOC queue

4) HTTP Request Action (to LimaCharlie if calling from Tines):
   - Method: POST
   - URL: https://api.limacharlie.io/v1/{{sid}}/isolation
   - Headers: Authorization: Bearer <LIMACHARLIE_API_KEY>
   - Body: {"reason":"Tines orchestration - automated containment"}
   - Check response code == 200 then continue to notify

Security:
- For incoming requests into Tines, use HMAC verification via the webhook secret (compute HMAC-SHA256 of the body and verify) — see Tines webhook docs for HMAC secret usage. :contentReference[oaicite:8]{index=8}

Slack integration:
- Use Tines Slack connect flow or Slack Incoming Webhook. To post from Tines use a Slack Action or an HTTP request to the Slack Incoming Webhook URL. :contentReference[oaicite:9]{index=9}

Notes:
- You can run the Flask demo locally and expose it with ngrok for Tines to call during testing.
- Replace `sid` values with real LimaCharlie sensor ids for actual isolation calls.
