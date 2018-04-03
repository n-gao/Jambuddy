import threading
import server
import time
from vst_reader import VstReader
from bpm_detector import BpmDetector
from suggestion_context import SuggestionContext
from pentatonic import get_note_name
import operator
from collections import deque
import pentatonic

override_bpm = None
current_key = None
difficulty = 0

ws_server, reader, bpm_d = None, None, None
suggestions = deque()

num_suggestions = 12

last_id = 0

class SuggestionNote:
    def __init__(self, note, bpm, time, key):
        global last_id
        self.id = last_id + 1
        last_id = last_id + 1
        self.bpm = bpm
        self.note = note
        self.note_name = pentatonic.get_note_name(self.note)
        self.time_to_play = time_to_play
        self.key = key

def get_suggestions(key, bpm, time):
    while len(suggestions) > 0 and (suggestions[0].time_to_play < time
        or suggestions[0].key != key):
        suggestions.pop()
    t_ = time
    with SuggestionContext('sqlite:///test.db') as db:
        while len(suggestions) < num_suggestions:
            sugg = db.get_random_suggestion(key[0], key[1])
            if sugg == None:
                return []
            for note in sugg.notes:
                t_ = t_ + note.delay * 60/bpm
                suggestions.append(SuggestionNote(
                    note.note,
                    bpm,
                    t_,
                    key
                ))
    return list(suggestions)[:num_suggestions]

def format_suggestions(to_format):
    suggs = []
    for sugg in to_format:
        suggs.append({
            'id' : sugg.id,
            'note' : sugg.note,
            'note_name' : sugg.note_name,
            'time_to_play' : sugg.time_to_play
        })
    return suggs


def get_info():
    if current_key is None:
        try:
            key_note, key_note_name, key_type = reader.get_key()
        except:
            key_note, key_note_name, key_type = None, None, None
    else:
        key_note, key_type = current_key
        key_note_name = pentatonic._base_notes[key_note]
    keys = reader.get_key_probabilities()
    bpm = bpm_d.get_bpm() if override_bpm is None else override_bpm
    t = time.time()
    to_transmit = get_suggestions((key_note, key_type), bpm, t)
    suggs = format_suggestions(to_transmit)
    return {
        'bpm' : bpm,
        'keys' : keys,
        'current_key' : {
            'key_note' : key_note,
            'key_type' : key_type,
            'key_name' : key_note_name,
            'probability' : 1
        },
        'time' : t,
        'difficulty' : difficulty,
        'suggestion_notes' : suggs,
        'suggestion_chords' : []
    }

async def set_difficulty(args):
    global difficulty
    difficulty = args['difficulty']
    return True

async def set_bpm(args):
    global bpm
    try:
        bpm = args['bpm']
    except:
        return False
    return True

async def set_key(args):
    global key
    try:
        key = (args['key_note'], args['key_type'])
    except:
        return False
    return True

methods = {
    'set_difficulty' : set_difficulty,
    'set_bpm' : set_bpm,
    'set_key' : set_key
}

def main():
    global ws_server, reader, bpm_d, methods
    ws_server = server.WebsocketServer(8888, methods)
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
        to_send = get_info()
        ws_server.send_to_all(to_send)
        time.sleep(1/2)
    server_thread._stop()
    reader_thread._stop()

if __name__ == '__main__':      
    main()
