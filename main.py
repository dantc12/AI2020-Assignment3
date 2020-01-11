from environment import Environment as Env
from helper_funcs import print_debug, print_query, print_info

ENVIRONMENT_SETTINGS_FILE = "environment_example.txt"

env = Env(ENVIRONMENT_SETTINGS_FILE)

print_info("OUR GRAPH:")
#print_info(env.graph)

print("------------------------------------------------")
print_debug("STARTING SIMULATION:")
env.simulation()
