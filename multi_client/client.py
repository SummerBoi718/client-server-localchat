import socket
import threading

clientName:str=""
def receive_messages(client_socket:socket.socket):
    
    while True:
        try:
            message:str=client_socket.recv(1024).decode()
            if not message:
                break
            print("\n"+message, end="\nYou>",flush=True)
        except (ConnectionResetError,ConnectionAbortedError):
            print("\n"+f"[Client]:>Disconnected from server.",end="\nYou>",flush=True)
            break
        except OSError:
            break

def start_client():
    global clientName
    client_socket:socket.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip:str="0.0.0.0"#specify the host ip here
    server_port:int=12345


    try:
        client_socket.connect((server_ip, server_port))
        print(f"Connected to server {server_ip}:{server_port}")

        receive_thread=threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()

        clientName=str(input("Enter name: "))
        client_socket.send(clientName.encode())

        while True:
            message=input("You>")
            
            if message.lower() == "exit":
                client_socket.send(b"exit")
                break
            client_socket.send(message.encode())

    except ConnectionRefusedError:
        print("Connection failed. Make sure the server is running.")
    
    finally:
        client_socket.close()
        print("Connection closed.")

start_client()
