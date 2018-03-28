import threading
import server
import time
from vst_reader import VstReader
from bpm import BpmDetector

def get_info():
    key_note, key_note_name, key_type = reader.get_key()
    return {
        'speed' : bpm_d.get_bpm(),
        'key_note' : key_note,
        'key_note_name' : key_note_name,
        'key_type' : key_type,
        'time' : time.time(),
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

ws_server, reader, bpm_d = None, None, None

def main():
    global ws_server, reader, bpm_d
    ws_server = server.WebsocketServer(8888)
    server_thread = threading.Thread(target=ws_server.start)
    server_thread.start()

    reader = VstReader('C:\\Users\\nicho\\\Desktop\\VSTHost\\vsthost.exe', 'C:\\Users\\nicho\\\Desktop\\VSTHost\\save.fxb')
    reader.reset()
    time.sleep(1/10)
    reader.fix_audio()
    reader_thread = threading.Thread(target=reader.continously_read)
    reader_thread.start()

    bpm_d = BpmDetector()
    bpm_thread = threading.Thread(target=bpm_d.continously_detect_bpm)
    bpm_thread.start()

    while True:
        ws_server.send_to_all(get_info())
        print(reader.get_key())
        print(bpm_d.get_bpm())
        time.sleep(1/30)
    server_thread._stop()
    reader_thread._stop()

if __name__ == '__main__':      
    main()
