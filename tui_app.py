from InquirerPy import prompt
from InquirerPy import inquirer
from InquirerPy.separator import Separator
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


def truncString(s, width):
    assert width>0, "width should be greater than zero."
    if len(s) > width:
        s = s[0:width] + "....."
    return s



class Tui:
    def __init__(self):
        self.included_tags = []
        self.excluded_tags = []
        self.data_handler = JH()
        self.max_string_length = 50

        self.actions_dict = {
                    "Include Tags" : self.includeTags,
                    "Exclude Tags" : self.excludeTags,
                    "View Song Info": self.viewSongInfo,
                    "Add Tags to Song" : self.addTagsToSong,
                    "Remove Tags From Song" : self.removeTagsFromSong,
                    "Exit" : self.quit
                    }

    def listSongs(self):
        # songs = self.data_handler.get_songs()
        # print(f"self.included_tags: {self.included_tags}")
        songs = self.data_handler.get_songs_with_tags(self.included_tags, self.excluded_tags)

        print(f"\n____________________Song List____________________")
        for item in idWithName(songs):
            print(truncString(item, self.max_string_length))
        print(f"_________________________________________________\n")
        print(f"Included Tags: {self.included_tags}\t Excluded Tags: {self.excluded_tags}")
        # print(f".................................................")

    
    def addTagsToSong(self):
        song = inquirer.fuzzy(
                message="Select Song: ",
                choices=idWithName(self.data_handler.get_songs().values()),
                default="",
                ).execute()

        song_id = getId(song)
        tags_in_song = self.data_handler.get_songs()[str(song_id)]["tags"]
        print(f"Current Tags: {tags_in_song}")

        tags = inquirer.select(
                message = "Tags : ",
                choices = list(self.data_handler.get_tags())  +[Separator(),"Add New Tag"],
                multiselect = True
                ).execute()
        
        if "Add New Tag" in tags:
            new_tag = inquirer.text(
                    message = "New Tag: ",
                    ).execute()
            tags.remove("Add New Tag")
            tags.append(new_tag)

        self.data_handler.add_tags(str(song_id), tags)
        print("[debug]: ",self.data_handler.get_songs()[str(song_id)])

    def removeTagsFromSong(self):
        song = inquirer.fuzzy(
                message="Select Song: ",
                choices=idWithName(self.data_handler.get_songs().values()),
                default="",
                ).execute()

        song_id = getId(song)
        tags_in_song = self.data_handler.get_songs()[str(song_id)]["tags"]
        print(f"Current Tags: {tags_in_song}")

        tags = inquirer.select(
                message = "Tags to Remove: ",
                choices = tags_in_song,
                multiselect = True
                ).execute()

        self.data_handler.remove_tags_from_song(str(song_id), tags)
        print("[debug]: ",self.data_handler.get_songs()[str(song_id)])
        
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

    def viewSongInfo(self):
        song = inquirer.fuzzy(
                message="Select Song: ",
                choices=idWithName(self.data_handler.get_songs().values()),
                default="",
                transformer = lambda x : truncString(x, self.max_string_length)
                ).execute()

        song_id = getId(song)
        song_data = self.data_handler.get_songs()[str(song_id)]
        print(f"Song\t: {truncString(song_data['name'], self.max_string_length)}")
        print(f"Artist\t: {song_data['artist']}")
        print(f"Tags\t: {song_data['tags']}")

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
