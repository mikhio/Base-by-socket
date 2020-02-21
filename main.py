import socket

URLS = {
	'/': '<h1>hello world</h1>',
	'/blog': '<h1>blog page</h1>'
}


def generate_headers(method, url):
	if not method == 'GET':
		return ('HTTP/1.1 405 Method not allowed\n\n', 405)

	if not url in URLS:
		return ('HTTP/1.1 404 Not found\n\n', 404)

	return ('HTTP/1.1 200 OK\n\n', 200)



def parse_request(request):
	parsed = request.split(' ')
	method = parsed[0]
	url = parsed[1] 

	return (method, url)


def generate_content(code, url):
	if code == 404:
		return '<h1>404</h1><h3>Not found</h3>'
	elif code == 405:
		return '<h1>405</h1><h3>Method not allowed</h3>'

	return URLS[url]


def generate_response(request):
	method, url = parse_request(request)
	headers, code = generate_headers(method, url)
	content = generate_content(code, url)

	return (headers + content).encode()


def run():
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind(('localhost', 5000))
	server_socket.listen()

	while True:
		client_socket, address = server_socket.accept()
		request = client_socket.recv(1024)
		print(request.decode('utf-8'))
		print()
		print(address)

		response = generate_response(request.decode('utf-8'))

		client_socket.sendall(response)
		client_socket.close()


if __name__ == '__main__':
	run()