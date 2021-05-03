# Q-Learning simulation code

This repo contains all the files to run the q-learner simulation on a cluster with PBS.

# Getting started

1. Clone https://git.hhu.de/werner01/qpricesim, build the wheel dist and install the package in the environment. The environment has to be found on the top-level of this repo.
   1. Note that if you work on a local university cluster, you might have to install the dependencies by yourself due to local network restrictions.
2. Run ```source clean_bld_folder.sh``` to create the build folder structure.
3. Run the specific PBS (job array) script for the simulations. The job array indices that you pass will be used as random seeds for a parameter grid that is derived from the specifications in parameters/parameter_{N}_agent_case.json.
4. After the grid search simulation finished you can find the super star agent my running ```python find_best_agent.py```. Then, run the super star simulation scripts.