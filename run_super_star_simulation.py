"""
For a given parameter set-up, we simulate the super star agents. Note that this module is
called directly with PBS where we use the job array index as a random seed value.

You need to pass two arguments, when calling this module.

1. File name of JSON file that is stored in the *parameters* folder, which
contains the all parameters for the simulation. The following keys have
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
    learning_rate (float): Learning rate for the super star agents.
    beta_decay (float): Decay parameter for the exploration rate
    simulation_periods (integer): How many rounds should be played upon convergence?
                                  Note that this is not used in this script but only
                                  later in the analysis.
    path_differ (string): Key word to use to differ the save files from
                          one to another.

"""
import json
import pickle
import sys

from qpricesim.model_code.QLearningAgent import jitclass_to_baseclass
from qpricesim.simulations.agents_simulation import train_agents


def sim_agents(parameter, random_seed_id):
    """
    A function to simulate a market with algorithmic agents. The random_seed_id will
    create different random seeds for each agent.

    Returns the state of convergence and the agents.


    Args:
        parameter (dict): Explained somewhere else TODO
        random_seed_id (integer): Integer which create unique random seeds for the agents.
                                  In my case this will be the job array index from PBS,
                                  such that the random seeds are different in each job
                                  array run.

    Returns:
        tuple: state, all_agents

               state (integer): State of convergence of the market/the agents
               all_agents (list): List of all QLearningAgents upon convergence
    """
    _, state, all_agents = train_agents(parameter=parameter, random_seed=random_seed_id)

    # Transform jitclass QLearned to no-jitted version
    # we need it to be able to pickle it later.
    trained_agents = []
    for agent in all_agents:
        trained_agents.append(jitclass_to_baseclass(agent_jit=agent))

    return state, trained_agents


if __name__ == "__main__":
    PATH_PARAMETER = sys.argv[1]
    JOB_ARRAY_INDEX = sys.argv[2]

    with open("./parameters/" + PATH_PARAMETER + ".json") as f:
        PARAMETER = json.load(f)
    print("Going to run with PARAMETER:")
    print(PARAMETER)

    # Run the simulation
    RESULTS = sim_agents(parameter=PARAMETER, random_seed_id=int(JOB_ARRAY_INDEX))

    OUT_PATH = "./bld/{}/super_stars/simulated_arrays_{}_seed_{}.pickle".format(
        PARAMETER["path_differ"], PARAMETER["path_differ"], JOB_ARRAY_INDEX
    )

    with open(OUT_PATH, "wb") as out_file:
        pickle.dump(RESULTS, out_file)
