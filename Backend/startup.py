import threading
import server
import time

def get_info():
    return {
        'test' : 'test'
    }

def main():
    ws_server = server.WebsocketServer(8888)
    server_thread = threading.Thread(target=ws_server.start)
    server_thread.start()
    while True:
        ws_server.send_to_all(get_info())
        time.sleep(1/30)
    server_thread.join()

if __name__ == '__main__':
    main()
