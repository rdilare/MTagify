- database: json file
- will contain list of songs
```json
{
"song_id": {
	"name": "song_name",
	"singer": "singer_name",
	"lyricist": "lyricist_name",
	"album": "album_name",
	"tags": ["tag_1", "tag_2",......,"tag_n"],	
	}

}
```

- each song will have options for adding, updating or deleting tags and other details.



## Tools
- flask app
- python-prompt-toolkit 
- PyInquirer



# Backend Design Components
- **json_handler**
  - maintain a json file
  - read data from json file
  - write data to json file

- **Model class**
  - define structur for songs details
  - will return dictionary object
   
- **songs_database**
  - CRUD feature
  - use: json_handler and song_model
  - addSong()
  - addTags()
  - getSongById()
  - getSongByTags()
