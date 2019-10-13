FROM python:2.7-alpine3.9
WORKDIR /usr/local/bin
COPY dotproxy.py .
CMD ["python","dotproxy.py"]