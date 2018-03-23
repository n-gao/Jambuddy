from suggestion_context import SuggestionContext

async def get_key(msg_obj):
    return 'C major'

async def get_bpm(msg_obj):
    return 120

async def get_suggestions(msg_obj):
    with SuggestionContext('sqlite:///test.db') as db:
        return db.get_random_suggestion(0).note_list

methods = {
    'get_key' : get_key,
    'get_bpm' : get_bpm,
    'get_suggestions' : get_suggestions
}
