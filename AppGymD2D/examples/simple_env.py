"""A simple example of how to use this environment.

Each step, GymD2D returns a dict of {agent_id: agent_observation}
    and requires a dict of {agent_id: actions}.
Agent rewards are also returned in a dict of {agent_id: agent_reward}.

The environment follows the Gym format of providing a game_over/terminal bool,
    but this will always be True as the environment is not episodic.
"""

import gym
import gym_d2d
import numpy as np
import json
import os
import psutil
import time
from pathlib import Path

cpu_start = psutil.cpu_percent() 
start = time.time()

def parse_info(k, info):
    str_data=str(info)
    #print(str_data)
    str_data = str_data.replace("'", "\"")
    # Insert line breaks before and after each curly brace to separate the objects
    str_data = str_data.replace('}{', '}\n{')
    #dict_data=json.loads(str_data)
    #print(dict_data)

    keys = [] #it will contain distinct object name that is Radio Base Stations
# this code is to find out distinct object names
    for line in str_data.splitlines():
        obj = json.loads(line)
        for key, value in obj.items():
            keys.append(key)
        break

    dict_data=json.loads(str_data)
    #file_info.write("slot-"+str(k)+'\n')
    capacity_due=[]
    capacity_cue=[]
    #print("Here: "+str(capacity_cue))
    j=0
    for i in keys:
        val=float(dict_data[i]['capacity_mbps'])
        if i.find("due")!=-1:
            #print("Due")
            capacity_due.append(val)
        else:
            #print("cue")
            capacity_cue.append(val)
        j+=1
        #file_info.write(i+" "+str(val)+'\n')
    file_info.write(str(k)+" "+str(np.mean(capacity_cue))+" "+str(np.std(capacity_cue))+" "+str(np.mean(capacity_due))+" "+str(np.std(capacity_due))+'\n')
    #file_info.write("Standard Deviation: "+" "+str(np.std(sum_capacity))+'\n')


        #print(i, ":", dict_data[i]['capacity_mbps'])

file_info=open('results.txt','r+')
for i in range(100):
    env_config = {'position_config_file': Path.cwd()/'position_config.json'}
    env = gym.make('D2DEnv-v0', env_config=env_config)
    #print('Run-', i)
    due_agent = 'DUEAgent()'
    game_over = False
    print("CPU util: ",psutil.cpu_percent())
    print("Mem. util: ",psutil.virtual_memory())
    for j in range(10):
        actions_dict = {}
        obses = env.reset()
        for agent_id, obs in obses.items():
            if agent_id.startswith('due'):
                action = env.action_space['due'].sample()
                # or action = due_agent.act(obs)
            elif agent_id.startswith('cue'):
                action = env.action_space['cue'].sample()
            else:
                action = env.action_space['mbs'].sample()
            actions_dict[agent_id] = action

        obses, rewards_dict, game_over, info = env.step(actions_dict)
        #print(info)
        parse_info(i*10+j, info)
        env.render()

cpu_end = psutil.cpu_percent()
cpu_diff = cpu_end - cpu_start
end = time.time()
print("CPU usage:", cpu_diff, "%") 
print("Total time: ", end-start)
