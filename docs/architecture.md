Architecture:

[Sensor / Endpoint] --> LimaCharlie EDR (events)
       |
       v (webhook or detection export)
[Tines SOAR] ----> (HTTP Request) ----> [Flask Orchestration Service (this repo) or directly call LimaCharlie]
       |                                      |
       |                                      v
       |                                  LimaCharlie API (POST /{sid}/isolation)
       |
       +--> Slack (alerts) & Email (alerting) for analysts and manual confirmation
