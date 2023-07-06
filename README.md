# AppGymD2D: It is a framework to evaluate application performance for a mobile D2D underlay network. 
AppGymD2D is built on top of an existing simulator called [GymD2D](https://github.com/davidcotton/gym-d2d). GymD2D is a toolkit for building, evaluating and comparing D2D cellular offload resource allocation algorithms.
It uses [OpenAI Gym](https://gym.openai.com/) to make it easy to experiment with many popular reinforcement learning or AI algorithms. 
It is highly configurable, allowing users to experiment with UE configuration, path loss and traffic models.

While GymD2D models a static D2D cellular offload scenario, AppGymD2D models a dynamic and mobile D2D underlay network. The framework models a single-cell scenario consisting of a macro base station surrounded with many cellular (CUE) and D2D (DUE) user equipment. The number of CUEs and DUEs may however change from time-to-time depending on the application requirements.

This project is still under active development and the API hasn't stabilised yet. 
Breaking changes are likely to occur between releases.

# Instructions for instalations:
Please follow [GymD2D](https://github.com/davidcotton/gym-d2d) for installation guide.

# Running a sample simulation:
The examples folder contain few python that can be directly run. A full fledged simulation can be run using the sim_env.py file.
Simply run the following code:
> python3 sim_env.py

to run the simulation.
# Steps to run the simulation.
1. Use BonnMotion to generate a trace file. Follow [BonnMotion](https://sys.cs.uos.de/bonnmotion/) to see how generate the trace file.
2. Convert the trace to .if format.
3. Run device_trace.py file to convert from .if to .tr format. .tr file contains mobility trace sorted on time-stamp.
4. Clear the track.txt file and write 0 (zero) into it. Note: file should not be empty or blank. This should be done after every run of simulation.
5. Initialize the num_cues and num_due_pairs parameters to appropriate values and other network parameters in the env_config.py file inside the envs folder. Note that the num_cues+2*num_due_pairs should be equal to the number of nodes for which the trace file was generated. For example, if the total number of nodes=90, then one possible value can be num_cue=20 and num_due_pairs=35. Other value may be possible. Also, num_cues must be >= 2 and should always be multiple of 2.
6. Place name of the trace file in simulator.py file (as of now it is har-coded). 
7. Do not empty the position.json file. It should contain atleast one record.
8. Now run the simulation using the above code.
  
# Contact:
For any queries, please contact: [Suvadip Batabyal](suvadip.batabyal@cse.nitdgp.ac.in)
