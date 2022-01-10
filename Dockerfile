FROM python:3.10.1-alpine
EXPOSE 8000

COPY . /app
WORKDIR /app
RUN rm -rf templates/static/*
COPY ./templates/static/dist /app/templates/static/dist

RUN apk --no-cache add --virtual builds-deps build-base gcc musl-dev python3-dev libffi-dev openssl-dev
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

CMD [ "gunicorn", "-b", "0.0.0.0:8000", "-w", "2", "main_run:app" ]