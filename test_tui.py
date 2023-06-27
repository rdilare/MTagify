from InquirerPy import prompt

from json_handler import JH


data_handler = JH()

songs = data_handler.get_songs()

def idWithName(songs_dict):
    result = []
    r = ""
    for song_data in songs_dict.values():
        r = str(song_data["id"]) + " : " + song_data["name"]
        result.append(r)
    return result


def getId(id_name_string):
    a = id_name_string.split(":")
    id = a[0].strip()
    return id


'''
n = 0
id = -1
for song_data in songs.values():
    print(f"song_name: {song_data['name']}")
    if n==13:
        id = str(song_data["id"])
    n+=1

print(f"song_details: {songs[id]}")
'''        


        
    
questions = [
    {
        "type": "input",
        "name": "name",
        "message": "what is your name?"
    },
    {
        "type": "list",
        "name": "color",
        "message": "select your favourite color",
        "choices": ["Red", "Blue", "Purple", "Green", "Yellow"]
    },
    {
        "type": "list",
        "name": "song",
        "message": "choose your song",
        # "choices": list(songs.values())[:10]
        "choices": idWithName(songs)
    }

]

answers = prompt(questions)

name = answers["name"]
color = answers["color"]
song_id = getId(str(answers["song"]))

print(f"name: {name}")
print(f"color: {color}")
print(f"song: {songs[song_id]}")