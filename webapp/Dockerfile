FROM python:3.12-alpine
ENV FLASK_APP test.py
ENV FLASK_CONFIG docker
RUN adduser -D Pollushow
USER Pollushow
WORKDIR /home/Pollushow
COPY requirements.txt requirements.txt
RUN python -m venv .venv
RUN venv/bin/pip install -r requirements.txt
COPY app app
COPY migrations migrations
COPY flasky.py config.py boot.sh ./
# runtime configuration
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]