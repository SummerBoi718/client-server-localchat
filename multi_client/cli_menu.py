import client, server

# user will be able to choose between hosting a room or joining a room

prompt:str="H:Host a Room | J:Join a Room | X:Exit > "



while True:
    choice:str=str(input(prompt)).lower()
    match choice:
        case "h":
            #call the server methods here
            print("Initiating server...")
            server.set_server_running(True)
            server.start_server()

        case "j":
            #call the client methods here
            print("Initiating client...")
            client.start_client()

        case "x":
            print("Exiting program...")
            break

        case _:
            print("Mode Unidentified.")



        