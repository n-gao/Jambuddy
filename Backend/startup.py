import threading
import server
import time

def main():
    ws_server = server.WebsocketServer(8888)
    server_thread = threading.Thread(target=ws_server.start)
    server_thread.start()
    while True:
        ws_server.send_to_all("hi")
    server_thread.join()

if __name__ == '__main__':
    main()
