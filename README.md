# AppGymD2D: It is a framework to evaluate application performance for a mobile D2D underlay network. 
AppGymD2D is built on top of an existing simulator called [GymD2D](https://github.com/davidcotton/gym-d2d). GymD2D is a toolkit for building, evaluating and comparing D2D cellular offload resource allocation algorithms.
It uses [OpenAI Gym](https://gym.openai.com/) to make it easy to experiment with many popular reinforcement learning or AI algorithms. 
It is highly configurable, allowing users to experiment with UE configuration, path loss and traffic models.

While GymD2D models a static D2D cellular offload scenario, AppGymD2D models a dynamic and mobile D2D underlay network. The framework models a single-cell scenario macro base station surrounded with many cellular (CUE) and D2D (DUE) user equipment. 

This project is still under active development and the API hasn't stabilised yet. 
Breaking changes are likely to occur between releases.

Please follow the installation requirements 
