import socket
import threading


clients={}
hostname:str=""
#to be implemented
def broadcast(client_socket, addr):
    global clients
    #when a client sends a msg to server the server will send it to
    #all connected clients except for the client that sent the message
    while True:
        try:
            #receive the data from clients first
            data = client_socket.recv(1024)
            if not data:
                break

            username:str=clients.get(client_socket)#get the sender's username
            message = data.decode().strip()

            # If client types "exit", broadcast that they left
            if message.lower() == "exit":
                leaveNotice = f"{username} has left the room."
                print("\n" + leaveNotice, end="\nYou>", flush=True)

                # Send leave message to all clients
                for client in list(clients.keys()):
                    if client != client_socket:
                        try:
                            client.send(leaveNotice.encode())
                        except BrokenPipeError:
                            pass

                break  # Exit the loop and remove the client


            formatted_message = f"{username}>{data.decode()}"
            #display the msg on the server first
            
            print("\n"+formatted_message, end="\nYou>",flush=True)

            #and then send the msg to all clients except sender
           
            for client in clients:
                if client != client_socket:
                    try:
                        client.send(formatted_message.encode())
                    except BrokenPipeError:#if client alr disconnected
                        pass
                

        except (ConnectionResetError, ConnectionAbortedError, OSError):
            break
    print("\n"+f"Connection closed with: {addr}",end="\nYou>",flush=True)
    # Remove client from dictionary before closing
    if client_socket in clients:
        del clients[client_socket]

    #clients.pop(client_socket, None)#this will remove the client obj in the dict and also its key
    client_socket.close()

def send_server_msg():
    global clients
    while True:
        message:str=input("You>")
        if message.lower()=="exit":
            print("Shutting down the server...")
            for client in list(clients.keys()):
                client.send(f"[Host]:{hostname}>Server is shutting down...".encode())
                client.close()
            clients.clear()
            break
        
        for client in list(clients.keys()):
            try:
                client.send(f"[Host]:{hostname}> {message}".encode())
            except BrokenPipeError:
                pass

def start_server():
    global clients
    global hostname
    servSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hostIp:str="0.0.0.0"
    hostPort:int=12345

    servSocket.bind((hostIp, hostPort))
    servSocket.listen(5)
    print(f"Server is listening on {hostIp}:{hostPort}")
    hostname=str(input("Enter hostname: "))

    #server input thread for server socket
    input_thread=threading.Thread(target=send_server_msg, daemon=True)
    input_thread.start()


    while True:
        try:
            cSocket,cAddr=servSocket.accept()
        
            username:str=cSocket.recv(1024).decode()
            clients[cSocket]=username

            #print("\n"+f"Client {username}:{cAddr} connected.",end="\nYou>",flush=True)

            join_message = f"{username} joined the room."
            print("\n"+join_message, end="\nYou>",flush=True)

            for client in clients:
                if client != cSocket:
                    client.send(join_message.encode())
            
            #start the broadcast thread
            broadcastThread = threading.Thread(target=broadcast, args=(cSocket, cAddr))
            broadcastThread.start()

        except KeyboardInterrupt:
            print("\nServer shutting down due to KeyboardInterrupt...")
            break

    servSocket.close()

start_server()