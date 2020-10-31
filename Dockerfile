FROM python:3

WORKDIR /usr/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP src/inicio.py

CMD [ "flask", "run" ]