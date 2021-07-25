import json

class Songdb():
	def __init__(self):
		self.data = {}
		self.filename = "data/user_data.json"
		
		self.loadData()

	def __del__(self):
		self.updateDB()

	def loadData(self):
		with open(self.filename) as f:
			data = f.read()
		self.data = json.loads(data)

	def updateDB(self):
		backup=''
		with open(self.filename,'r') as f:
			backup = f.read()
		with open(self.filename+".bak",'w') as f:
			f.write(backup)
		with open(self.filename,'w') as f:
			json.dump(self.data,f,indent = 4)
			print("DB updated")


	def getData(self):
		return self.data

	def getSongById(self,id):
		for song in self.data["songs"]:
			if song["id"]==id:
				return song

	def getSongsWithTags(self,*tags):
		songs = []
		for song in self.data['songs']:
			for tag in tags:
				for s_tag in song["tags"]:
					if s_tag.upper()==tag.upper():
						songs.append(song)
		return songs

	def addTags(self,*tags,songname=None):
		if not songname:
			raise Exception("song name is not given")
		for i,song in enumerate(self.data['songs']):
			if song['name']==songname:
				if not song.get('tags'):
					self.data['songs'][i].update({'tags':[*tags]})
					self.updateDB()
					return
				for tag in tags:
					flag = False
					for s_tag in song['tags']:
						if tag.upper()==s_tag.upper():
							flag = True
							break
					if not flag:
						# tag_list = self.data['songs'][i]['tags']
						# tag_list.append()
						self.data['songs'][i]['tags'].append(tag)
		self.updateDB()


	def addSong(self,name,artist=None):
		id = len(self.data)+1
		self.data['songs'].append({"name":name,"artist":artist,"id":id})
		self.updateDB()