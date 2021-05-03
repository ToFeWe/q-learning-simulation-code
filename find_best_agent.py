"""

A module to find the agent amongst all simulations
that has the highest weighted average profitability.

The output is written to a JSON File for the super star simulations
but also to pickle, as we want to use it in the experiment with
humans.
"""
import json
import pickle
from copy import copy
from os import walk

import numpy as np


def load_simulation_data(file_path):
    """
    Load and return all files which are stored in the directory *file_path*.


    Args:
        file_path (string): Full path to the folder with all
                            simulation results pickles for a given specification.

    Returns:
        list: List of tuples, where each tuple represents the super star output
              for a given simulation. The tuples have the following ordering:

              trained_agents[0] (QLearningAgent): The super star of the simulation
                                                  (first agent of its market).
              alpha (float): Learning rate of the super star.
              beta (float): Decay parameter for epsilon-greedy algorithm
              weighted_profitability (array): Array with the weighted profitability
                                              for each agent in the given super star market.
              best_response_share (array): Array with the best response share
                                           for each agent in the given super star market.
              profitability_state (array): Array with the profitability in the state of
                                           convergence for each agent in the given super
                                           star market.
              avg_profit (array): Array with the average profitability
                                  for each agent in the given super star market.
              state (integer): Index/Integer representation of the state of convergence
                               of the super star market.
              random_seeds (list): List of random seeds used for the given super star
                                   market.

    """

    # Get all files
    all_files = []
    for (dirpath, dirnames, filenames) in walk(file_path):
        all_files.extend(filenames)
        break

    # Load the files
    simulation_results = []
    for file in all_files:
        in_path = file_path + file
        with open(in_path, "rb") as f:
            simulation_results.append(pickle.load(f))

    # Unroll the dicts
    all_dicts = [d.values() for d in simulation_results]

    # TODO: Add a check here that all simulations are used and the seeds are all
    # unique
    return all_dicts


def get_all_best_agents(file_path):
    """
    Load in all files that are stored under
    the given file path and  returns the simulation
    results arrays.
    Note that all files stored under the *file_path*
    should be pickles as returned by the grid search
    simulation.

    Args:
        file_path (string): Path to the folder containing the simulation
                            output files.

    Returns:
        list: List with QLearningAgents that achieved the best average weighted
              profitability within their respective simulation run.
    """
    all_simulation_dicts = load_simulation_data(file_path=file_path)

    # Super stars are always the last element in the output
    all_super_stars = list(zip(*all_simulation_dicts))[-1]
    return all_super_stars


def get_the_best_agent(file_path):
    """

    Get the agent that has the highest weighted profitability.
    """
    # Get all good agents among all simulations
    all_good_agents = get_all_best_agents(file_path)

    # Avg weigthed profit has the index 3 (4th position) in the
    # tuple *all_good_agents*
    INDEX_AVG_PROFIT = 3

    # Find the simulation which has the agents with the highest average weighted profitability.
    # Note that we average this for all agents in the simulation, to curb the influence of
    # outliers.
    max_avg_weighted_profits = (
        np.vstack(list(zip(*all_good_agents))[INDEX_AVG_PROFIT]).mean(axis=1).max()
    )
    for agent_specs in all_good_agents:
        if agent_specs[INDEX_AVG_PROFIT].mean() == max_avg_weighted_profits:
            return agent_specs


if __name__ == "__main__":
    for n_agent in [2, 3]:
        OUT_FILE_PATH_JSON = f"./parameters/parameter_super_star_{n_agent}_agent.json"
        OUT_FILE_PATH_PICKLE = (
            f"./bld/{n_agent}_agents/experiment_super_star_{n_agent}_agent.pickle"
        )
        BASE_PARAMETER_FILE_PATH = f"./parameters/parameter_{n_agent}_agent_base.json"
        SIMULATION_FILE_PATH = f"./bld/{n_agent}_agents/grid_search/"

        with open(BASE_PARAMETER_FILE_PATH) as f:
            parameter_base = json.load(f)

        # Get the best agent for the market with n_agent players
        best_agent_output = get_the_best_agent(file_path=SIMULATION_FILE_PATH)

        # Alpha of the best agent is in index position 1
        alpha_best_agent = best_agent_output[1]

        # Beta of the best agent is in index position 2
        beta_best_agent = best_agent_output[2]

        parameter_super_star_simulation = copy(parameter_base)
        parameter_super_star_simulation["learning_rate"] = alpha_best_agent
        parameter_super_star_simulation["beta_decay"] = beta_best_agent
        parameter_super_star_simulation["path_differ"] = f"{n_agent}_agents"

        # Write the super star parameter file to disc for the
        # super star simulations.
        with open(OUT_FILE_PATH_JSON, "w") as f:
            json.dump(parameter_super_star_simulation, f, indent=4)

        with open(OUT_FILE_PATH_PICKLE, "wb") as f:
            pickle.dump(best_agent_output, f)
