FROM python:3.10-slim

# Add non-root user
RUN useradd worker
USER worker
WORKDIR /home/worker

COPY --chown=worker sms.py requirements.txt README.md LICENSE ./

RUN pip --no-cache-dir install -r requirements.txt

CMD [ "python", "-u", "sms.py" ]