import socket
import threading
import ipPort_resolver

clients={}
hostname:str=""
server_running = False#global flag to control server
roomPassword:str=""
def broadcast(client_socket, addr):
    global clients
    #when a client sends a msg to server the server will send it to
    #all connected clients except for the client that sent the message
    while server_running:
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

                break

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

    
    client_socket.close()
    #print(f"The server_running value is {server_running}")
    
def send_server_msg():
    global clients
    global server_running


    while True:
        message:str=input("You>")
        if message.lower()=="exit":
            print("Shutting down the server...")
            server_running = False
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

def set_server_running(val:bool):
    global server_running
    server_running = val

def set_room_password():
    global roomPassword
    while True:
        password:str=input("Enter a password must be 6 chars: ")
        if (len(password)) >= 6:
            roomPassword = password
            print(f"Password set to [{password}:[{roomPassword}]]")
            break
        else:
            print(f"[password] is an invalid password!")

def ask_password(client_socket)->bool:
    tries:int=3
    prompt:str=f"Please enter the room Password({tries}): ".encode()
    while tries != 0:
        client_socket.send(prompt)
        response:str=client_socket.recv(1024).decode()
        if response == roomPassword:
            client_socket.send("200".encode())
            return True
            
        else:
            tries -= 1
            if tries == 0:
                client_socket.send("404".encode()) 
                client_socket.close()
                return False
            else:
                client_socket.send("304".encode())

def start_server():
    global clients
    global hostname
    servSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    valid_ip_and_port:bool=False
    while not valid_ip_and_port:


        hostIp:str=ipPort_resolver.get_ip("Enter IP to bind the server to; e.g. 0.0.0.0: ")
        valid_ip:bool=ipPort_resolver.is_valid_ip(ip=hostIp)


        hostPort:int=ipPort_resolver.get_port("Enter Port to listen to, must be > 1024; e.g. 12345:")
        valid_port:bool=ipPort_resolver.is_valid_port(port=hostPort)

        valid_ip_and_port=valid_ip and valid_port

    servSocket.bind((hostIp, hostPort))
    servSocket.listen(5)
    servSocket.settimeout(1.0)
    print(f"Server is listening on {hostIp}:{hostPort}")

    hostname=str(input("Enter hostname: "))

    set_room_password()

    #server input thread for server socket
    input_thread=threading.Thread(target=send_server_msg, daemon=True)
    input_thread.start()
    

    while server_running:
        try:
            cSocket,cAddr=servSocket.accept()

            if not ask_password(cSocket):
                continue

            username:str=cSocket.recv(1024).decode()
            clients[cSocket]=username

            

            join_message = f"{username} joined the room."
            print("\n"+join_message, end="\nYou>",flush=True)

            for client in clients:
                if client != cSocket:
                    client.send(join_message.encode())
            
            #start the broadcast thread
            broadcastThread = threading.Thread(target=broadcast, args=(cSocket, cAddr))
            broadcastThread.start()
        
        except socket.timeout:
            continue

        except KeyboardInterrupt:
            print("\nServer shutting down due to KeyboardInterrupt...")
            break
    
    servSocket.close()
    print("Server shutdown complete.")
