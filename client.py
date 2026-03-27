import socket

HOST = '127.0.0.1'   # change to server IP for multi-laptop
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((HOST, PORT))
except:
    print("❌ Server not available")
    exit()

while True:
    print("\n1. View Seats")
    print("2. Book Seat")
    print("3. Cancel Seat")
    print("4. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        client.send("VIEW".encode())
        print("Seat Status:", client.recv(1024).decode())

    elif choice == "2":
        seat = input("Enter seat number (0-4): ")
        client.send(f"BOOK {seat}".encode())
        print(client.recv(1024).decode())

    elif choice == "3":
        seat = input("Enter seat number to cancel (0-4): ")
        client.send(f"CANCEL {seat}".encode())
        print(client.recv(1024).decode())

    elif choice == "4":
        break

    else:
        print("Invalid choice")

client.close()