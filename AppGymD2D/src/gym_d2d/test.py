import json
import os

class Device_to_json:

	def __init__(self, total_devices):
		global json_file
		self.total_devices=100
		self.trace_file=open('sorted.tr','r')
		self.json_file=open('./envs/device_config.json','r+')
		self.file_position=0
		self.cues=30
		self.due_pairs=10

	def create_json(self, i:int, x:float, y:float)->None:
		data={"due"+f'{i:02d}' :
			{
				"position" : 
				[
					x,
					y
				]
			}
		}
		self.json_file.seek(0, os.SEEK_END)
		print("File size", self.json_file.tell())
		if self.json_file.tell()==0:
			print("Here")
			dictionary=[
				{
					"num_cues" : str(self.cues),
					"num_due_pairs" : str(self.due_pairs)
				}
			]
			json_object = json.dumps(dictionary, indent=4)
			self.json_file.write(json_object)

		
		self.json_file.seek(0,0)
		file_data = json.load(self.json_file)
		file_data.append(data)
		self.json_file.seek(0)
		json.dump(file_data, self.json_file, indent = 4)

	def append_to_json(self)->None:
		print("called")
		#self.trace_file.seek(self.file_position,0)
		for i in range(self.total_devices):
			line=self.trace_file.readline()
			words=line.split(" ")
			x=words[2]
			y=words[3].replace("\n","")
			print(float(x))
			print(float(y))
			#y=int(y)
			self.create_json(i, x, y)
		#self.file_position=self.trace_file.tell()

	def _truncate(self)->None:
		self.json_file.truncate(0)

#json_file=0
device=Device_to_json(100)
device.append_to_json()
device._truncate()
device.append_to_json()
print(int("09"))
