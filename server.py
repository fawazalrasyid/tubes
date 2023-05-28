import socket  # Mengimpor modul socket untuk komunikasi jaringan
import os  # Mengimpor modul os untuk operasi sistem

def get_file(path):
    with open(path, 'rb') as file:
        return file.read()  # Membaca dan mengembalikan isi file yang diberikan oleh path

def handle_http_request(request):
    method, path, _ = request.split('\n')[0].split()
    path = path[1:]
    if path == "":
        path = "index.html"
    if method == "GET":
        try:
            content = get_file(path)  # Membaca konten file jika path yang diminta ada
            response_header = "HTTP/1.1 200 OK\r\n"  # Header respons dengan status 200 OK
            response = f"HTTP/1.1 200 OK\r\n\r\n".encode('utf-8') + content  # Respons dengan status 200 OK dan konten file
        except FileNotFoundError:
            content = get_file("404.html")  # Jika path tidak ditemukan, gunakan file "404.html"
            response_header = "HTTP/1.1 404 Not Found"  # Header respons dengan status 404 Not Found
            response = f"HTTP/1.1 404 Not Found\r\n\r\n".encode('utf-8') + content  # Respons dengan status 404 Not Found dan konten file
    else:
        content = get_file("405.html")  # Jika metode bukan GET, gunakan file "405.html"
        response_header = "HTTP/1.1 405 Method Not Allowed"  # Header respons dengan status 405 Method Not Allowed
        response = f"HTTP/1.1 405 Method Not Allowed\r\n\r\n".encode('utf-8') + content  # Respons dengan status 405 Method Not Allowed dan konten file

    return response_header, response  # Mengembalikan header respons dan respons

def start_web_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Membuat soket TCP
    server_address = ('localhost', 8080)  # Alamat dan port server
    server_socket.bind(server_address)  # Bind soket ke alamat dan port tertentu
    server_socket.listen(1)  # Listen koneksi masuk dengan antrian sebanyak 1
    print('Server is running on http://{}:{}'.format(server_address[0], server_address[1]))  # Menampilkan pesan server telah dimulai

    while True:
        client_socket, client_address = server_socket.accept()  # Menerima koneksi dari klien
        print('Menerima koneksi dari: {}'.format(client_address))  # Menampilkan pesan koneksi diterima

        request = client_socket.recv(1024).decode('utf-8')  # Menerima permintaan dari klien

        response_header, response = handle_http_request(request)  # Menangani permintaan dan mendapatkan respons

        method, req, protocol = request.split('\n')[0].split()  # Memisahkan metode, permintaan, dan protokol dari permintaan
        filepath = os.path.join(os.getcwd(), request.split()[1][1:])  # Menggabungkan direktori kerja saat ini dengan path file yang diminta
        print('Method   : {}'.format(method))  # Menampilkan metode permintaan
        print('Request  : {}'.format(req))  # Menampilkan permintaan
        print('Path     : {}'.format(filepath))  # Menampilkan path file yang diminta
        print('Protocol : {}'.format(protocol))  # Menampilkan protokol permintaan
        print('Respone  : {}'.format(response_header))  # Menampilkan header respons
        print("\n-------------------------------------------------\n")

        client_socket.sendall(response)  # Mengirim respons ke klien
        client_socket.close()  # Menutup koneksi dengan klien

if __name__ == '__main__':
    start_web_server()  # Memulai web server
