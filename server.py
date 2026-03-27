import socket
import threading
import time

HOST = '0.0.0.0'
PORT = 5000

seats = [0, 0, 0, 0, 0]
lock = threading.Lock()

MAX_CLIENTS = 5   # optimization: limit clients

def handle_client(conn, addr):
    print(f"[CONNECTED] {addr}")

    while True:
        try:
            data = conn.recv(1024).decode()

            if not data:
                break

            start_time = time.time()   # performance start
            print(f"{addr} -> {data}")

            command = data.split()

            # VIEW seats
            if command[0] == "VIEW":
                conn.send(str(seats).encode())

            # BOOK seat
            elif command[0] == "BOOK":
                try:
                    seat = int(command[1])

                    if seat < 0 or seat >= len(seats):
                        conn.send("INVALID seat number".encode())
                        continue

                    with lock:
                        if seats[seat] == 0:
                            seats[seat] = 1
                            response = "SUCCESS Seat booked"
                        else:
                            response = "FAILED Seat already booked"

                    conn.send(response.encode())

                except:
                    conn.send("ERROR Invalid input".encode())

            # CANCEL seat
            elif command[0] == "CANCEL":
                try:
                    seat = int(command[1])

                    if seat < 0 or seat >= len(seats):
                        conn.send("INVALID seat number".encode())
                        continue

                    with lock:
                        if seats[seat] == 1:
                            seats[seat] = 0
                            response = "CANCELLED"
                        else:
                            response = "Seat already free"

                    conn.send(response.encode())

                except:
                    conn.send("ERROR Invalid input".encode())

            else:
                conn.send("UNKNOWN COMMAND".encode())

            # performance end
            end_time = time.time()
            print(f"[PERFORMANCE] Response time: {end_time - start_time:.6f} sec")

        except:
            break

    print(f"[DISCONNECTED] {addr}")
    conn.close()


# create server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("🚀 Reservation Server Started...")

while True:
    conn, addr = server.accept()

    # optimization: limit clients
    if threading.active_count() - 1 >= MAX_CLIENTS:
        conn.send("Server busy, try later".encode())
        conn.close()
        continue

    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()

    print("Active clients:", threading.active_count() - 1)
