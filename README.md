# Q-Learning simulation code

This repo contains all the files to run the q-learner simulation on a cluster with PBS.

# Getting started
1. Clone this package.
2. Move to the top-level and create a new virtual environment called *q_env*.
3. Clone https://git.hhu.de/werner01/qpricesim, build the wheel dist and install the package in the environment. 
   1. Note that if you work on a local university cluster, you might have to install the dependencies by yourself due to local network restrictions.
4. Run ```source clean_bld_folder.sh``` to create the build folder structure.
5. Run the specific PBS (job array) script for the simulations. The job array indices that you pass will be used as random seeds for a parameter grid that is derived from the specifications in parameters/parameter_{N}_agent_case.json.
   1. The script will try to run the tests for the *qpricesim* package which is assumed to be on top-level folder, in which you also created the environment.
6. After the grid search simulation finished you can find the super star agent my running ```python find_best_agent.py```. Then, run the super star simulation scripts.
7. TODO to run the replication package you need to reduce the files to a single file. This is best done on a cluster too given the memory TODO