import random

total_devices=90
no_of_groups=3

def randomize(total:int):
	global total_devices
	total_devices=total
	device_grp=total_devices/no_of_groups
	print(device_grp)
	due_pairs=random.randint(1,device_grp/2)
	cues=device_grp-2*due_pairs
	return cues, due_pairs

def write_to_json(c_usrs:int, d_usrs:int, total_devices:int)->list:
	global cues, dues
	grp_size=int(c_usrs+d_usrs*2)
	cues=int(c_usrs)
	dues=int(d_usrs*2)
	due_list={}
	cue_list={}
	start=0
	for i in range(no_of_groups):
		lst=list(range(start, start+grp_size)) #shuffle the entire group
		random.shuffle(lst)
		due_list[i]=lst[:dues]
		cue_list[i]=lst[-cues:]
		print("DUEs: ",due_list[i])
		print("CUEs", cue_list[i])
		start+=int(total_devices/no_of_groups)
	
	return due_list, cue_list



cues, due_pairs = randomize(total_devices)
print(cues, due_pairs)
d_lst, c_lst=write_to_json(cues, due_pairs, total_devices)
if 5 in d_lst[0]:
	print("DUE")
else:
	print("CUE")
print(d_lst[0][3])
#print(c_lst)