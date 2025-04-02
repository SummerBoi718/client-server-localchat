import socket

def get_ip(prompt: str) -> str:
    return input(prompt)

def get_port(prompt: str) -> int:
    try:
        return int(input(prompt))
    except ValueError:
        return None

def is_valid_ip(ip: str) -> bool:
    
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        print("Invalid Ip address supplied")
        return False
    

def is_valid_port(port: int) -> bool:
   #ensuring the port entered is not withing da privileged range
   try:
       if port >= 1024 and port <= 65535:
           return True
       else:
           print("Invalid Port number supplied")
           return False
       
   except (ValueError, TypeError):
       print("The port supplied must be int")
       return False

