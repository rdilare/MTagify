from InquirerPy import prompt
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from functools import partial
import copy

from json_handler import JH


# data_handler = JH()
# songs = data_handler.get_songs()


def idWithName(songs_list):
    result = []
    r = ""
    for song_data in songs_list:
        r = str(song_data["id"]) + " : " + song_data["name"]
        result.append(r)
    return result


def getId(id_name_string):
    a = id_name_string.split(":")
    id = a[0].strip()
    return id




class Tui:
    def __init__(self):
        self.included_tags = []
        self.excluded_tags = []
        self.data_handler = JH()
        self.actions_dict = {
                    "Search" : self.searchSong,
                    "Include Tags" : self.includeTags,
                    "Exclude Tags" : self.excludeTags,
                    "Exit" : self.quit
        }

    def listSongs(self):
        # songs = self.data_handler.get_songs()
        print(f"self.included_tags: {self.included_tags}")
        songs = self.data_handler.get_songs_with_tags(self.included_tags, self.excluded_tags)

        print(f"___songs_list______________________________________")
        for item in idWithName(songs)[:10]:
            print(item)
        print(f"___________________________________________________\n")

    
    def searchSong(self):
        song = inquirer.fuzzy(
        message="Select Song:",
        choices=idWithName(self.data_handler.get_songs().values()),
        default="",
        ).execute()

        song_id = getId(song)

        print(self.data_handler.get_songs()[str(song_id)])
        
    def includeTags(self):
        tags = inquirer.checkbox(
            message="Included tags:",
            # choices = self.data_handler.get_tags(),
            choices = [ Choice(i, name = i, enabled = i in self.included_tags) for i in self.data_handler.get_tags()],
            # validate=lambda result: len(result) >= 1,
            # invalid_message="should be at least 1 selection",
            # instruction="(select at least 1)",
        ).execute()
        self.included_tags = tags

    def excludeTags(self):
        tags = inquirer.checkbox(
            message = "Excluded tags:",
            # choices = self.data_handler.get_tags(),
            choices = [ Choice(i, name = i, enabled = i in self.excluded_tags) for i in self.data_handler.get_tags()],
            # validate=lambda result: len(result) >= 1,
            # invalid_message="should be at least 1 selection",
            # instruction="(select at least 1)",
        ).execute()
        self.excluded_tags = tags

    def quit(self):
        return "exit"
    
    def getMainOptions(self):
        return self.actions_dict.keys()

    

    def runApp(self):
        while True:
            self.listSongs()
            print("===================================================================\n\n")
            action = inquirer.select(
            message = "Main Menu", choices = self.getMainOptions()
            ).execute()
            res = self.actions_dict[action]()
            # print(f"option: {self.included_tags}")


            if res == "exit":
                break

if __name__=="__main__":
    app = Tui()
    app.runApp()
