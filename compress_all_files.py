"""

A script to load all files to take all files from the different random seeds
and compress them into one file.
"""

import pickle
from os import walk


def load_folder_files(file_path):
    """
    A function to load all files in a given
    directory and return it as a list.
    Note that its assumed that in the folder
    all files are pickle files.

    Args:
        file_path (string): Path to the files

    Returns:
        list: List of elements that were stored in the
              the pickle files.
    """
    # Get all files
    all_files = []
    for (dirpath, dirnames, filenames) in walk(file_path):
        all_files.extend(filenames)
        break

    # Load the files
    out_results = []
    for file in all_files:
        in_path = file_path + "/" + file
        with open(in_path, "rb") as f:
            out_results.append(pickle.load(f))

    return out_results

def load_grid_simulation_data(file_path):
    """
    Load all files from the grid search simulation which are stored in the
    directory *file_path* and write them to a list of lists.
    Each list then contains the arrays for all simulation


    Args:
        file_path (string): Path to the simulation files

    Returns:
        list: list of list with the outcome arrays
              for all MC simulation.

              Ordered the following way:
              list[0]: Arrays of the convergence state profitability
              list[1]: Arrays with the weighted profitability
              list[2]: Arrays with the best response shares
              list[3]: Array with the average profitability
              list[4]: Array with the average price after convergence
              list[5]: Array with the Nash equilibria
              list[6]: Array with all best action responses
              list[7]: Array with prices before and after shocking the market
              list[8]: All super star agents in the grid search
    """
    # Get all files
    simulation_results = load_folder_files(file_path=file_path)

    # Unroll the dictionaries
    all_dicts = [d.values() for d in simulation_results]

    # TODO: Add a check here that all simulations are used and the seeds are all
    # unique
    # TODO: Similar Code used in simulation part which is NOT in waf
    # Should be refactored!
    return all_dicts


def sim_results_to_dict(file_path):
    """

    Returns the simulation results arrays.


    Args:
        file_path (string): Path to the simulation files

    Returns:
        dict: Dict with all simulation results arrays
    """
    all_simulation_dicts = load_grid_simulation_data(file_path=file_path)

    # Dropping the super star tuple here.
    (
        state_profitability_array,
        weighted_profitability_array,
        best_response_share_array,
        avg_profit_array,
        avg_price_array,
        nash_equilibrium_array,
        all_best_actions_array,
        periods_shock_array,
        _,
    ) = zip(*all_simulation_dicts)

    all_arrays = {}
    all_arrays["state_profitability"] = state_profitability_array
    all_arrays["weighted_profitability"] = weighted_profitability_array
    all_arrays["best_response_share"] = best_response_share_array
    all_arrays["avg_profit"] = avg_profit_array
    all_arrays["avg_price"] = avg_price_array
    all_arrays["nash_equilibrium"] = nash_equilibrium_array
    all_arrays["all_best_actions"] = all_best_actions_array
    all_arrays["periods_shock"] = periods_shock_array

    return all_arrays

if __name__ == '__main__':
    for n_agents in [2, 3]:
        print("Running for ", n_agents, " agents")
        SIMULATION_FILE_PATH = f"./bld/{n_agents}_agents/grid_search/"
        all_arrays = sim_results_to_dict(file_path=SIMULATION_FILE_PATH)
        for key, value in all_arrays.items():
            print("Saving the file for ", key)
            with open(f"./bld/{n_agents}_agents/grid_{n_agents}_agents_{key}.pickle", "wb") as f:
                pickle.dump(value, f)