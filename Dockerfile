FROM python:2.7-alpine3.9
WORKDIR /usr/local/bin
COPY dotproxy.py .
#Run app
CMD ["python","dotproxy.py"]
