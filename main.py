from environment import Environment as Env
from helper_funcs import print_debug, print_query, print_info

ENVIRONMENT_SETTINGS_FILE = "environment_large_example2.txt"

print_query("Please enter K vehicle loss penalty value:")
k_val = raw_input()
# k_val = 2
if str(k_val) == '':
    env = Env(ENVIRONMENT_SETTINGS_FILE)
else:
    env = Env(ENVIRONMENT_SETTINGS_FILE, int(k_val))


print_info("OUR GRAPH:")
print_info(env.graph)

print_query("The number of agents in the environment will be 2.")
num_of_agents = 2
agent_options = ["Adversarial (zero sum game)", "Semi-cooperative", "Fully cooperative"]
print_query("Please enter agent type:")
for j in range(len(agent_options)):
    print_info(str(j + 1) + ". " + agent_options[j])
choice = input() - 1
# choice = 1
ag_type = agent_options[choice]

print_query("Please enter starting position (starting vertex number) of A1:")
a1_s_vertex = env.graph.vertices[input()-1]
# a1_s_vertex = env.graph.vertices[0]
print_query("Please enter starting position (starting vertex number) of A2:")
a2_s_vertex = env.graph.vertices[input()-1]
# a2_s_vertex = env.graph.vertices[2]
print_query("Please enter the cutoff value:")
cutoff_val = raw_input()
# cutoff_val = 9999999
if str(cutoff_val) == '':
    env.add_agents(ag_type, a1_s_vertex, a2_s_vertex)
else:
    env.add_agents(ag_type, a1_s_vertex, a2_s_vertex, int(cutoff_val))

print "------------------------------------------------"
print_debug("STARTING SIMULATION:")
env.simulation()
