
import os
import sys
from chatbotQuery.io.parameters_processing import parse_configuration_file,\
    create_tables, create_graphs


def auto_testing(configuration_file):
    parameters = parse_configuration_file(configuration_file)
    states_list_table, path_states, xstates, transitions =\
        create_tables(parameters)
    treestates, graphs_statemachines, complete_network =\
        create_graphs(states_list_table, path_states, xstates, transitions)


if __name__ == "__main__":
    args = sys.argv
    configuration_file = args[1]
    assert(os.path.isfile(configuration_file))
    auto_testing(configuration_file)
