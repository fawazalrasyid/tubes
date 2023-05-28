import socket # Mengimpor modul socket untuk komunikasi jaringan

def get(server_address, filename):
    # Membuat soket klien
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)  # Menghubungkan soket klien ke alamat server

    # Membuat string permintaan
    request = f"GET /{filename} HTTP/1.1\r\nHost: {server_address[0]}\r\n\r\n"
    client_socket.send(request.encode())  # Mengirim permintaan ke server
    print("Request sent\n")

    print("HTTP Response:\n")

    data = ""
    while True:
        client_socket.settimeout(5)  # Mengatur waktu tunggu soket
        newData = client_socket.recv(1024).decode()  # Menerima data dari server dan menguraikannya dari byte menjadi string
        if not newData:  # Jika tidak ada data yang diterima lagi
            break
        data += newData  # Menyimpan data yang diterima
    print(data)  # Menampilkan data yang diterima dari server

    client_socket.close()  # Menutup soket klien setelah selesai

if __name__ == "__main__":
    server_address = ('localhost', 8080)
    filename = input("Nama File yang Dicari: ")
    get(server_address, filename)  # Memanggil fungsi get dengan alamat server dan nama file yang dimasukkan pengguna