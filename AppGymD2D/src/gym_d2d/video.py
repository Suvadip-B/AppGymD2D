class video:
	def _init_(self, size, pop, _id):
		self.id=_id		#unique ID of a video
		self.size=size=10*random.randint(1,9)		#size in MB
		self.pop=1               #default value of popularity is 1, which is highest
		self.cached=-1			#will denote the node-id where a video is cached; -1, if not cached
		

	def play (self, rate, time)->bool:
		if(self.size-rate*time>0):
			self.size=self.size-rate*time
			return false
		else:
			self.size=0
			return true

	def idCached(self,vid)->int:
		if self.cached==-1:
			return -1
		else:
			return self.cached


