import json


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
            print(f"data: {self.data}")
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
        print(self.data,"\n")
        song_data_ = {"name": song_name, "artist": artist_name}
        self.add_data(song_data_)
        print(self.data)


    def add_tags(self, tags=[]):
        if not tags:
            return
    
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

    def get_data(self):
        return self.data

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
        with open(self.db_filename,"r") as f:
            data = f.read()
            if not data:
                is_data = False
        with open(self.db_filename,"a") as f:
            if not is_data:
                template = {"songs": {"id": {"name" : "None", "artist":"None", "id":"None"}}} 
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


x = JH()
print("\nbefore",x.get_data())
x.add_song("song_1", "artist_1")
x.add_song("song_2", "artist_2")
# song = x.remove_by_id("2")
# print("\nsong: ",song)
print("after\n",x.get_data())

x.print_songs()
