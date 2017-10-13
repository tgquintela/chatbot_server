
import os
import sys
from chatbotQuery.ai import create_trainning_transition


if __name__ == "__main__":
    args = sys.argv
    configuration_file = args[1]
    out_filepath = args[2] if len(args) > 2 else ''
    assert(os.path.isfile(configuration_file))
    create_trainning_transition(configuration_file, out_filepath)
