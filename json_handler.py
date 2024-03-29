import json
import sys


template = {
  "songs": {
    "id": {
      "name": "None",
      "artist": "None",
      "id": "None"
    },
    "0": {
      "name": "name_2",
      "artist": "artist_2",
      "id": 0
    }
  },
  "tags_map": {
      "tag1":0,
      "tag2":0,
  }
}

song_data_structure = {
                        "name": "None",
                        "artist": "None",
                        "id":"id",
                        "tags":[]
                        }

class JH:
    def __init__(self):
        self.db_filename = "data.json"
        self.data = dict()
        self.prev_data = dict()
        self.create_file()
        self.load()
        for field, value in song_data_structure.items():
            self.add_field(field, value)

    def load(self):
        with open(self.db_filename,"r") as f:
            self.data = json.load(f)
            # print(f"data: {self.data}")
            self.prev_data = self.data

        with open(self.db_filename+".bak", "w") as f:
            json.dump(self.prev_data, f, indent=2)

    def add_data(self,data):
        if not "songs" in self.data.keys():
            self.data.update({"songs":{}})
        if not isinstance(data, dict):
            raise TypeError("data must be of dict type")
        if "id" in self.data["songs"].keys():
            self.data["songs"].pop("id")
        if "id" in list(data.keys()):
            data_id = data["id"]
        else:
            data_id = self.get_new_id()
            data.update({"id":data_id})

        song_data = song_data_structure.copy()
        song_data.update(data)
        self.data["songs"].update({str(data_id):song_data})
        # self.data["songs"].append({data})
        self.save_to_file()

    def add_song(self, song_name, artist_name="unknown"):
        # print(self.data,"\n")
        song_data_ = {"name": song_name, "artist": artist_name}
        self.add_data(song_data_)
        # print(self.data)


    def add_tags(self, song_id, tags=[]):
        song_data = self.data["songs"][str(song_id)]
        # print(f"[debug]: {song_data}")
        for tag in tags:
            if not tag in self.data["tags_map"].keys():
                self.data["tags_map"].update({str(tag):0})

            if not tag in song_data["tags"]:
                self.data["songs"][str(song_id)]["tags"].append(str(tag))
                self.data["tags_map"][str(tag)]+=1
        # print(f"[debug]: {song_data}")

        self.save_to_file()
    
    def add_field(self, field, value):
        for key in self.data["songs"].keys():
            if not field in self.data["songs"][key].keys():
              self.data["songs"][key].update({field: value})
        self.save_to_file()


    def remove_by_id(self,song_id):
        song = {}
        if song_id in self.data.keys():
            song = self.data.pop(song_id)
            self.save_to_file()
        return song
    
    def remove_tags_from_song(self, song_id, tags):
        for tag in tags:
            song_data = self.data["songs"][str(song_id)]
            if tag in song_data["tags"]:
                song_data["tags"].remove(tag)
                self.data["tags_map"][tag]-=1
        self.save_to_file()

    def get_songs(self):
        return self.data["songs"]
    
    def get_tags(self):
        return self.data["tags_map"].keys()
    
    def get_songs_with_tags(self, included_tags=[], excluded_tags=[]):
        song_list = []
        for song_data in self.data["songs"].values():
            should_add = False
            for tag in included_tags:
                if tag in song_data["tags"]:
                    should_add = True
                    break
            for tag in excluded_tags:
                if tag in song_data["tags"]:
                    should_add = False
                    break
            if should_add:
                song_list.append(song_data)
        return song_list


    def get_new_id(self):
        return len(self.data["songs"].keys())

        keys = list(self.data["songs"].keys())
        new_id = ""
        current_id = 0
        for i in range(len(keys)-1):
            current_id = int(keys[i])
            if int(keys[i+1])-int(keys[i])>1:
                break
        if not len(keys):
            new_id = str(current_id)
        elif current_id==int(keys[-2]):
            new_id = str(int(keys[-1])+1)
        else:
            new_id = str(current_id+1)
        return new_id

    def create_file(self):
        is_data = True
        try:
            with open(self.db_filename,"r") as f:
                data = f.read()
                if not data:
                    is_data = False
        except FileNotFoundError:
            print("not file as data.json. creating file")
            is_data = False

        with open(self.db_filename,"a") as f:
            if not is_data:
                # template = {"songs": {"id": {"name" : "None", "artist":"None", "id":"None"}}} 
                template = {"songs": {"id": song_data_structure}, "tags_map":{}} 
                # template = {}           
                json.dump(template, f, indent=2)
                print("creating file: data.json")
            else:
                print("file is already there")

    def save_to_file(self):
        with open(self.db_filename,"w") as f:
            json.dump(self.data, f, indent=2)

    def print_songs(self):
        for song_data in self.data["songs"].values():
            print(f"song \t: {song_data['name']}")
            print(f"artist \t: {song_data['artist']}")
            print(f"id \t: {song_data['id']}\n")



def file_to_data(filename, data_handler):
    with open(filename,"r") as f:
        for line in f:
            print(f">> {line}")
            data_handler.add_song(line.strip())

def __del__(self):
    print("destructor called")
    self.save_to_file()
            



if __name__=="__main__":
    x = JH()    
    # x.print_songs()
    x.add_tags(0,["hindi","sad"])
    x.add_tags(1,["sad", "hopeless"])
    x.add_tags(2,["sad", "hopeless", "hindi"])

    song_list = x.get_songs_with_tags(included_tags=["happy", "sad"], excluded_tags=["inspiration"])

    for song_data in song_list:
        print(f"{song_data}\n")


    '''
    x.remove_tags_from_song(0,["sad"])
    x.add_song("song_1", "artist_1")
    x.add_song("song_2", "artist_2")
    # song = x.remove_by_id("2")
    # print("\nsong: ",song)

    '''
    # x.print_songs()


    '''
    if len(sys.argv)<2:
        raise Exception("provide filename")
    filename = sys.argv[1]
    print(filename)
    file_to_data(filename, x)
    '''
