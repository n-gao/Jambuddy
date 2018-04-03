# Documentation
Server running at:
```
ws://localhost:8888
```

Send data:
```
{
    "speed" : float,
    "keys : Key[],
    "current_key" : Key,
    "time" : float,
    "difficulty" : String,
    "suggestion_notes" : Note[],
    "suggestion_chords" : Chord[]
}
```

Key:
```
{
    "key_note" : int,
    "key_name" : String,
    "key_type" : String,
    "probabilitiy" : float
}
```

Note:
```
{
    "id" : int,
    "note" : int,
    "note_name"  : String,
    "time" : float
}
```

Chord:
```
{
    "id" : int,
    "chord" : int,
    "chord_name" : String,
    "time" : float
}
```
