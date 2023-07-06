import json
import random
import os
import linecache

from pathlib import Path
from typing import Optional, Type

total_devices:int=0
no_of_groups:int=0
cues=0
dues=0


def randomize(total:int, n_groups:int):
	global total_devices, no_of_groups
	total_devices=total
	no_of_groups=n_groups
	device_grp=total_devices/no_of_groups
	due_pairs=random.randint(1,device_grp/2)
	cues=device_grp-2*due_pairs
	if cues==0:
		cues=2
		due_pairs=due_pairs-1
	return cues, due_pairs

def write_to_json(c_usrs:int, d_usrs:int, total_devices:int)->list:
	global cues, dues
	grp_size=int(c_usrs+d_usrs*2)		#multiply by 2 to get no. of DUE devices
	cues=int(c_usrs)
	dues=int(d_usrs*2)
	due_list={}
	cue_list={}
	start=0
	for i in range(no_of_groups):
		lst=list(range(start, start+grp_size)) #shuffle the entire group
		random.shuffle(lst)
		due_list[i]=lst[:dues]
		if cues!=0:
			cue_list[i]=lst[-cues:]
		#print("DUEs: ",due_list[i])
		#print("CUEs", cue_list[i])
		start+=int(total_devices/no_of_groups)

	return due_list, cue_list

class Device_to_json:

	def __init__(self, trace_file:str, json_file:str, c_lst, d_lst):
		self.cue_list=c_lst
		self.due_list=d_lst
		self.grp_size=int(total_devices/no_of_groups)
		self.trace_file=open(trace_file,'r')
		self.json_file=open(json_file,'r+')
		self.file_position=0
		self.track=open('./track.txt', 'r+')			# This file tracks the lines that are read from .tr file

	def create_json(self, i:int, _type:str, x:float, y:float)->None:
		data={_type+f'{i:03d}' :
				{
					"position" : 
					[
						x,
						y
					]
				}
			}

		dictionary=[
					{_type+f'{i:03d}' :
						{
							"position" : 
							[
								x,
								y
							]
						}
					}
					]
			
		self.json_file.seek(0, os.SEEK_END)
		#print("File size", self.json_file.tell())
		if self.json_file.tell()==0:
			#print("Here")
			json_object = json.dumps(dictionary, indent=4)
			self.json_file.write(json_object)
		else:
			self.json_file.seek(0,0)
			file_data = json.load(self.json_file)
			file_data.append(data)
			self.json_file.seek(0)
			json.dump(file_data, self.json_file, indent = 4)
			self.json_file.seek(0,0)

	def append_to_json(self)->None:
		self.track=open('./track.txt', 'r+')
		self.trace_file.seek(int(self.track.readline()))
		for i in range(total_devices):
			k=int(i/self.grp_size)
			line=self.trace_file.readline()
			words=line.split(" ")
			x=words[2]
			y=words[3].replace("\n","")
			if i in self.cue_list[k]:
				d_type="cue"
			else:
				d_type="due"
			self.create_json(i, d_type, x, y)
		self.track.truncate(0)
		self.track.seek(0,0)
		self.track.write(str(self.trace_file.tell()))
		self.track.close()

	def load_position_config(self) -> dict:
        	return json.load(self.json_file)

	def _truncate(self)->None:
		self.json_file.truncate(0)
		self.json_file.seek(0,0)
