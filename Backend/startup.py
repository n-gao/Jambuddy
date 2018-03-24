import threading
import server
import time

def get_info():
    return {
        'speed' : 120,
        'key_note' : 5,
        'key_note_name' : 'C',
        'key_type' : 'major',
        'time' : 0,
        'suggestion' : [
            {
                'note' : 53,
                'note_name' : 'D5',
                'time' : 0.25
            },
            {
                'note' : 58,
                'note_name' : 'G5',
                'time' : 0.5
            },
            {
                'note' : 29,
                'note_name' : 'D3',
                'time' : 0.75
            },
            {
                'note' : 27,
                'note_name' : 'C3',
                'time' : 1
            }
        ],
        # OR
        'suggestion_notes' : [53, 58, 29, 27],
        'suggestion_note_names' : ['D5', 'G5', 'D3', 'C3'],
        'suggestion_times' : [0.25, 0.5, 0.75, 1]
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
