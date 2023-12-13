"""

A module that is called directly by PBS to run the
simulation on algorithmic collusion.

You need to pass three arguments, when calling this module.

1. File name of JSON file that is stored in the *parameters* folder, which
contains the basic parameters for the simulation. The following keys have
to be specified in  the JSON.
    n_agent (integer): Number of algorithmic agent to consider
    k_memory (integer): Length of the memory of the agent, i.e. how many
                        periods do they remember.
    discount_rate (float): Discount rate for all agents.
    exploration_rate (float): Exploration rate. Note that this is not actually used
                              as we use epsilon decay to determine it. TODO
    min_price (integer): Minimal price that can be played in the market.
    max_price (integer): Maximal price that can be played in the market.
    reservation_price (integer): Highest price the consumer are willing to pay.
    m_consumer (integer): Number of consumers in the market.
    step (integer): Steps between the prices
    learning_iterations (integer): Maximal number of learning iterations if we do
                                   not converge before.
    rounds_convergence (integer): Number of periods the best action in each state has to stay
                                  the same for us to conclude that the agent converged.
    Q_star_threshold (float): Convergence rule when solving the known MDP, when deriving the
                              optimal q matrix for an agent.

2. File name of JSON file that is stored in the *parameters* folder, which
contains the parameters for the simulation, that define the parameter grid
for the learning rate and the decay parameter. The following keys have
to be specified in  the JSON.
    beta_max (float): Minimal beta (exploration decay) we consider in the
                      grid search.
    beta_min (float): Maximal beta (exploration decay) we consider in the
                      grid search.
    alpha_min (float): Minimal alpha (learning rate) we consider in the
                       grid search.
    alpha_min (float): Maximal alpha (learning rate) we consider in the
                       grid search.
    grid_points (integer): Number of grid points to consider for both,
                           alpha and beta.
    path_differ (string): Key word to use to differ the save files from
                          one to another.

3. An integer value which is used to create unique random seeds for all
agents. In my case this is usually the job array index from PBS. The
whole simulation is parallized with respect to the monte carlo repetitions.
"""
import json
import pickle
import sys

from qpricesim.simulations.mc_simulation_job_array import run_single_simulation


if __name__ == "__main__":
    PATH_PARAMETER_BASE = sys.argv[1]
    PATH_PARAMETER_CASES = sys.argv[2]
    JOB_ARRAY_INDEX = sys.argv[3]

    with open("./parameters/" + PATH_PARAMETER_BASE + ".json") as f:
        PARAMETER_BASE = json.load(f)
    with open("./parameters/" + PATH_PARAMETER_CASES + ".json") as f:
        PARAMETER_CASES = json.load(f)
    print("Going to run with BASE:")
    print(PARAMETER_BASE)
    print("BASE Parameter:")
    print(PARAMETER_CASES)

    RESULTS = run_single_simulation(
        base_parameter=PARAMETER_BASE,
        cases=PARAMETER_CASES,
        job_array_index=JOB_ARRAY_INDEX,
    )

    OUT_PATH = "./bld/{}/grid_search/simulated_arrays_{}_seed_{}.pickle".format(
        PARAMETER_CASES["path_differ"], PARAMETER_CASES["path_differ"], JOB_ARRAY_INDEX
    )

    with open(OUT_PATH, "wb") as out_file:
        pickle.dump(RESULTS, out_file)
