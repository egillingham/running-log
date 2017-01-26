FROM python:2.7
MAINTAINER Erin <e.gillingham9@gmail.com>

RUN mkdir -p /var/log/gunicorn/ && mkdir /opt/website

WORKDIR /opt/website

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY website/ .

CMD ["gunicorn", "app:APP", "-c", "gunicorn-config.py"]

