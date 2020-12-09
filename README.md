OVERVIEW
-------------

Here is simple DNS over TLS proxy server.
I choose SocketServer python library as the clear and easy way
to implement such kind of solution. Cloudflare used as DNS over TLS server. 
Other services could be used as well and redefined in DNS_HOST, DNS_PORT global variables.
Incoming tcp connections handling by MyTCPHandler class. tcp_connection_to(DNS_HOST) establish secure
connection to DNS server. On every new tcp connection TCPHandler call dns_proxy() which re-send accepted data
and return dns query result back to TCPHandler.

HOW TO RUN
-------------

* Pre-conditions: Docker and docker-compose (>1.18.0) installed.

This proxy was designed as containerized service.
Clone source code to separate folder and run commands below in same folder.
One button deploy -
```
docker-compose up -d --build
```

Now you could test it with dig (one if the most popular dns query tool):
```
dig @localhost -p 8053 n26.com +tcp
```

Security concerns:
-------------
DNS queries could be impacted by the man-in-the-middle attack.


Microservice architecture:
-------------
Proxy is already dockerized and could be implemented in containerized cluster.
In high-load infrastructure environment may be it's better to hide it behind reverse-proxy service 
and use celery+redis to quick multiple response.

Possible improvements:
-------------
As this is example solution, there are a lot of thinks that could be implemented
- Aggregating log of each connection
- Cashing same old queries to speed-up response
- Choose or use different DNS services (not only cloudflare) with passing variables on proxy start-up

Multiple connections could be easly implemented with ThreadingMixIn class - https://docs.python.org/2/library/socketserver.html
UDP handler could be added as well with same proxy flow (listen to UDP connections to, wrap income data to send it over TCP)
