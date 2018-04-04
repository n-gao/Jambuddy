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
from chord_suggestion import get_random_chord
import random

override_bpm = 30
current_key = None
difficulty = 0

ws_server, reader, bpm_d = None, None, None
sugg_notes = deque()
sugg_chords = deque()

num_suggestions = 12

last_id = 0

class SuggestionChord:
    def __init__(self, chord, time_to_play, key):
        global last_id
        self.id = last_id + 1
        last_id = last_id + 1
        self.chord, self.chord_type = chord
        self.chord_name = pentatonic.ind_to_note[self.chord]
        self.time_to_play = time_to_play
        self.key = key

class SuggestionNote:
    def __init__(self, note, time_to_play, key):
        global last_id
        self.id = last_id + 1
        last_id = last_id + 1
        self.note = note
        self.note_name = pentatonic.get_note_name(self.note)
        self.time_to_play = time_to_play
        self.key = key

def get_chord_suggestions(key, bpm, time):
    global sugg_chords
    while len(sugg_chords) > 0 and (sugg_chords[0].time_to_play < time
        or sugg_chords[0].key != key):
        sugg_chords.popleft()
    t_ = sugg_chords[-1].time_to_play if len(sugg_chords) > 0 else time
    if key[0] is None:
        return []
    while len(sugg_chords) < num_suggestions:
        chord = get_random_chord(key)
        if chord is None:
            return []
        delay = 1
        for i in range(4):
            t_ = t_ + delay * 60/bpm
            sugg_chords.append(SuggestionChord(
                chord,
                t_,
                key
            ))
    return list(sugg_chords)[:num_suggestions]


def get_note_suggestions(key, bpm, time):
    global sugg_notes
    while len(sugg_notes) > 0 and (sugg_notes[0].time_to_play < time
        or sugg_notes[0].key != key):
        sugg_notes.popleft()
    if len(sugg_chords) > 0:
        t_ = sugg_notes[-1]
    else:
        t_ = time
    if not all(key):
        return []
    with SuggestionContext('sqlite:///test.db') as db:
        while len(sugg_notes) < num_suggestions:
            sugg = db.get_random_suggestion(key[0], key[1])
            for note in sugg.notes:
                t_ = t_ + note.delay * 60/bpm
                sugg_notes.append(SuggestionNote(
                    note.note,
                    t_,
                    key
                ))
    return list(sugg_notes)[:num_suggestions]

def format_note_suggestions(to_format):
    suggs = []
    for sugg in to_format:
        suggs.append({
            'id' : sugg.id,
            'note' : sugg.note,
            'note_name' : sugg.note_name,
            'time_to_play' : sugg.time_to_play
        })
    return suggs

def format_chord_suggestions(to_format):
    suggs = []
    for sugg in to_format:
        suggs.append({
            'id' : sugg.id,
            'chord' : sugg.chord,
            'chord_type' : sugg.chord_type,
            'chord_name' : sugg.chord_name,
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
    if difficulty == 0:
        suggestion_chords = get_chord_suggestions((key_note, key_type), bpm, t)
        suggestion_notes = []
    else:
        suggestion_notes = get_note_suggestions((key_note, key_type), bpm, t)
        suggestion_chords = []
    suggs_n = format_note_suggestions(suggestion_notes)
    suggs_c = format_chord_suggestions(suggestion_chords)
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
        'suggestion_notes' : suggs_n,
        'suggestion_chords' : suggs_c
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
    # reader.reset()
    # time.sleep(1/10)
    # reader.fix_audio()
    reader_thread = threading.Thread(target=reader.continously_read)
    reader_thread.start()

    bpm_d = BpmDetector()
    bpm_thread = threading.Thread(target=bpm_d.continously_detect_bpm)
    bpm_thread.start()

    while True:
        to_send = get_info()
        ws_server.send_to_all(to_send)
        time.sleep(1/1)
    server_thread._stop()
    reader_thread._stop()

if __name__ == '__main__':      
    main()
