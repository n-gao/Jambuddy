# Documentation
Server running at:
```
ws://localhost:8888
```

## Outgoing data:

You get this information block 10 times per second:
```
{
    "bpm" : float,
    "keys" : Key[],
    "current_key" : Key,
    "time" : float,
    "difficulty" : ENUM(0: Beginner, 1: Advanced),
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
    "probability" : float
}
```

Note:
```
{
    "id" : int,
    "note" : int,
    "note_name"  : String,
    "time_to_play" : float
}
```

Chord:
```
{
    "id" : int,
    "chord" : int,
    "chord_type" : String,
    "chord_name" : String,
    "time_to_play" : float
}
```

## Incoming messages:
All messages have the following type:
```
{
    "method" : String,
    "args" : {
        ...
    }
}
```

Where method can be one of the following:
```
{
    "method" : "set_difficulty",
    "args" : {
        "difficulty" : ENUM(0: Beginner, 1: Advanced)
    }
}
```
```
{
    "method" : "set_bpm",
    "args" : {
        "bpm" : float
    }
}
```
```
{
    "method" : "set_key",
    "args" : {
        "key_note" : int,
        "key_type" : String
    }
}
```
