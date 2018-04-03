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

class PlaySuggestion:
    def __init__(self, sugg, bpm, time, key):
        self.time = time
        self.bpm = bpm
        self.sugg = sugg
        self.key = key
        self.notes = self.sugg.note_list
        self.times = []
        last_t = self.time
        for n in self.sugg.notes:
            last_t = last_t + n.delay * 60/self.bpm
            self.times.append(last_t)
        self.note_names = list(map(get_note_name, self.notes))

    @property
    def last_note(self):
        return self.times[-1]

def check_suggestions(key_note, key_note_name, key_type, bpm, time):
    while len(suggestions) > 0 and (suggestions[0].last_note < time
        or suggestions[0].key != key_note_name):
        suggestions.pop()
    t_ = time
    while len(suggestions) < 10:
        with SuggestionContext('sqlite:///test.db') as db:
            sugg = db.get_random_suggestion(key_note, key_type)
            p_sugg = PlaySuggestion(sugg, bpm, t_, key_note_name)
            t_ = p_sugg.last_note
            suggestions.append(p_sugg)

def format_suggestions(to_format, time):
    suggs = []
    for sugg in to_format:
        for i in range(len(sugg.notes)):
            if sugg.times[i] >= time:
                note = sugg.notes[i]
                note_name = sugg.note_names[i]
                _time = sugg.times[i]
                suggs.append({
                    'note' : note,
                    'note_name' : note_name,
                    'time' : _time
                })
    return suggs


def get_info():
    if current_key is None:
        key_note, key_note_name, key_type = reader.get_key()
    else:
        key_note, key_type = current_key
        key_note_name = pentatonic._base_notes[key_note]
    keys = reader.get_key_probabilities()
    bpm = bpm_d.get_bpm() if override_bpm is None else override_bpm
    t = time.time()
    check_suggestions(key_note, key_note_name, key_type, bpm, t)
    to_transmit = list(suggestions)[:3]
    notes, note_names, times, suggs = format_suggestions(to_transmit, t)
    return {
        'bpm' : bpm,
        'keys' : keys,
        'current_key' : {
            'key_note' : key_note,
            'key_type' : key_type,
            'key_name' : key_note_name,
            'probability' : 1
        }
        'time' : t,
        'difficulty' : difficulty,
        'suggestion_notes' : suggs,
        'suggestion_chords' : []
    }

ws_server, reader, bpm_d = None, None, None
suggestions = deque()

async def set_difficulty(args):
    global difficulty
    difficulty = args['difficulty']

async def set_bpm(args):
    global bpm
    bpm = args['bpm']

async def set_key(args):
    global key
    key = (args['key_note'], args['key_type'])


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
        to_send = get_info()
        ws_server.send_to_all(to_send)
        time.sleep(1/2)
    server_thread._stop()
    reader_thread._stop()

if __name__ == '__main__':      
    main()
