import SocketServer
import socket
import ssl


def tcp_connection_to(DNS_HOST):
    #Create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(100)

    #Wrap socket
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations('/etc/ssl/certs/ca-certificates.crt')
    wrappedSocket = context.wrap_socket(sock, server_hostname=DNS_HOST)

    #Establish connection
    wrappedSocket.connect((DNS_HOST, DNS_PORT))
    return wrappedSocket


def dns_proxy(data, DNS_HOST):
    # Establish connection and send DNS query
    tls_connection = tcp_connection_to(DNS_HOST)
    tls_connection.send(data)

    #Save response from DNS server
    dns_result = tls_connection.recv(1024)

    if dns_result:
        return dns_result
    else:
        return "INVALID DNS QUERY"


class MyTCPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()

        #Save dns proxy result
        res = dns_proxy(self.data, DNS_HOST)

        self.request.sendall(res)


if __name__ == "__main__":
    DNS_HOST, DNS_PORT = "1.1.1.1", 853
    HOST, PORT = "10.10.10.2", 53

    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()


