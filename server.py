import socket
import threading

HOST = '0.0.0.0'   # allows multiple devices
PORT = 5000

seats = [0, 0, 0, 0, 0]   # 5 seats (0 = free, 1 = booked)
lock = threading.Lock()

def handle_client(conn, addr):
    print(f"[CONNECTED] {addr}")

    while True:
        try:
            data = conn.recv(1024).decode()

            if not data:
                break

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

                    # critical section (concurrency control)
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
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()

    print("Active clients:", threading.active_count() - 1)