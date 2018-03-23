import asyncio

async def get_key(msg_obj):
    return 'C major'

async def get_bpm(msg_obj):
    return 120

async def get_suggestions(msg_obj):
    return [0, 1, 2, 3, 4]

methods = {
    'get_key' : get_key,
    'get_bpm' : get_bpm,
    'get_suggestions' : get_suggestions
}