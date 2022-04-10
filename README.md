# ZTE SMS to Email

Read received SMS from ZTE modem and submit to Mailgun API. After email submited, remove SMS message from modem storage.

Tested with ZTE MF823D.

## Usage

Copy `.env.example` to `.env` and configure environment variables.

```
cp .env.example .env
docker run -d --env-file .env --restart always ghcr.io/olkitu/zte-sms-to-email
```