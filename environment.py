from graph import Graph
from helper_funcs import print_debug, print_info, print_query
import timeit


class Environment:

    P_LEAKAGE = 0.001

    def __init__(self, config_file_path):
        self.graph = Graph(config_file_path)
        self.env_time = 0

        self.dead_ppl = 0
        self.total_ppl = self.graph.get_ppl2save()

        # Environment.PERCEPT = self

        print_debug("CREATED ENVIRONMENT WITH " + str(self.graph.num_of_vertices()) + " VERTICES, AND " +
                    str(self.graph.num_of_roads()) + " ROADS.")

    ###############################
    def update(self):
        pass
    ###############################

    # def get_people_array_considering_deadlines(self):
    #     res = self.graph.get_people_array()
    #     for i in range(len(res)):
    #         if self.graph.vertices[i].deadline < self.env_time:
    #             res[i] = 0
    #     return res

    ###############################
    def simulation(self):
        start = timeit.default_timer()
        print_debug("PRINTING ENVIRONMENT STATUS:")
        self.print_env()

        self.env_time = self.env_time + 1
        print "------------------------------------------------"

        stop = timeit.default_timer()
        print_debug("GAME OVER --- TIME: " + str(round(stop - start, 2)) + "s")
        print_info("PRINTING ENVIRONMENT STATUS:")
        self.print_env()
    ###############################

    ###############################
    def print_env(self):
        print_info("TIME IS: " + str(self.env_time))

        print_info("OUR VERTICES TYPES:")
        v_types = []
        for vertex in self.graph.vertices:
            v_types.append(vertex.v_type)
        print_info(str(v_types))

        print_info("OUR VERTICES PEOPLE COUNT: ")
        people_arr = self.graph.get_people_array_with_shelter()
        print_info(str(people_arr))

        ppl_saved = sum([v.ppl_count for v in self.graph.vertices if v.is_shelter()])
        print_info("PEOPLE SAVED: " + str(ppl_saved) + "/" + str(self.total_ppl))
    ###############################