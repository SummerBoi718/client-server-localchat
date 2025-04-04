import socket
import threading
import ipPort_resolver
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
def send_password(client_socket):
    while True:
        try:
            prompt = client_socket.recv(1024).decode()
            if not prompt:
                break
            response = input(prompt)
            client_socket.send(response.encode())

            serverResponse = client_socket.recv(1024).decode()
            if serverResponse == "200":
                print("Correct password! Joining room...")
                break
            elif serverResponse == "304":
                print("Incorrect password. Try again.")
            elif serverResponse == "404":
                print("No more attempts left. Connection will close.")
                client_socket.close()
                return False
        except:
            print("Password validation failed or connection closed.")
            return False

        


def start_client():
    global clientName
    client_socket:socket.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    valid_ip_and_port:bool=False
    while not valid_ip_and_port:
        

        server_ip:str=ipPort_resolver.get_ip("Enter IP of the server you want to join; e.g. 192.168.63.0 : ")
        valid_ip:bool=ipPort_resolver.is_valid_ip(server_ip)

        server_port:int=ipPort_resolver.get_port("Enter Port to listen to, must be > 1024; e.g. 12345: ")
        valid_port:bool=ipPort_resolver.is_valid_port(server_port)
        valid_ip_and_port=valid_ip and valid_port

    try:
        client_socket.connect((server_ip, server_port))
        print(f"Connected to server {server_ip}:{server_port}")
        send_password(client_socket)

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
    except (BrokenPipeError, ConnectionResetError):
        print("Cant send message as server's already closed.")
    except OSError:
        print("Connection to the server denied.")
        client_socket.close()
    finally:
        client_socket.close()
        print("Connection closed.")
    client_socket.close()
    print("Client closed")

