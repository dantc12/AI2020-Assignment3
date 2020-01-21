import bayesNetwork
from graph import Graph
from bayesNetwork import bayesNetwork
from helper_funcs import print_debug, print_info, print_query
import timeit


class Environment:
    def __init__(self, config_file_path):
        self.graph = Graph(config_file_path)
        self.env_time = 0
        self.bayesNet = bayesNetwork(self.graph)

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
        evidenceList = []
        inp = 1
        while 1 <= inp <= 3:
            print_query("Enter what you want to do:")
            print_query("\t1. Add piece of evidence to evidence list.")
            print_query("\t2. Do probabilistic reasoning.")
            print_query("\t3. Reset evidence list to empty")
            print_query("\t4. Quit the program.")
            inp = int(input())

            if inp == 1:
                print_info("You chose to add evidence.")
                print_info("Examples of evidence input:")
                print_info("\tFlooding at vertex 1 at time 1 -> V11")
                print_info("\tEdge 2 not blocked at time 0 -> not E20")
                print_query("Enter evidence:")
                ev = str(input()).split()
                if len(ev) is 1:
                    evidenceVar = self.bayesNet.getBayesNodeByName(ev[0])
                    evidenceList.append(bayesNetwork.VarWithVal(evidenceVar, True))
                else:
                    evidenceVar = self.bayesNet.getBayesNodeByName(ev[1])
                    evidenceList.append(bayesNetwork.VarWithVal(evidenceVar, False))

            elif inp == 2:
                print_info("You chose to do probabilistic reasoning. Choose your query:")
                print_query("\t1. What is the probability that each of the vertices is flooded?")
                print_query("\t2. What is the probability that each of the edges is blocked?")
                print_query("\t3. What is the probability that a certain path (set of edges) is free from blockages?")
                print_query("\t4. BONUS: What is the path between 2 given vertices that has" +
                            " the highest probability of being free from blockages at time t=1?")
                print_query("\t5. Go back.")
                query_choice = int(input())
                print_info("Given our evidence: " + str([str(ev) for ev in evidenceList]))
                if query_choice == 1:
                    self.bayesNet.query_floodings(evidenceList)
                elif query_choice == 2:
                    self.bayesNet.query_blockages(evidenceList)
                elif query_choice == 3:
                    print_query("Enter Path:")
                    print_query("\tFor example: E11 E21")
                    pathElements = str(input()).split()
                    path = []
                    for edge in pathElements:
                        pathElement = self.bayesNet.getBayesNodeByName(edge)
                        path.append(pathElement)

                    res = self.bayesNet.query_pathNotBlocked(path, evidenceList)
                    print_info("P(Path not blocked = True) = " + str(res))
                elif query_choice == 4:
                    print_query("Enter 2 vertices:")
                    print_query("\tFor example: V1 V4")
                    pathElements = str(input()).split()
                    v1 = self.graph.get_vertex_from_string(pathElements[0])
                    v2 = self.graph.get_vertex_from_string(pathElements[1])
                    path, prob = self.bayesNet.getBestRoute(v1, v2, evidenceList)
                    print_query("Best path is: " + self.bayesNet.get_path_str(path) + " with probability: " + str(prob))
                    X=1
                    pass

            elif inp == 3:
                evidenceList = []
                # paths = self.graph.get_paths(self.graph.get_vertex(1), self.graph.get_vertex(4), [self.graph.get_vertex(1)], [])
                # for p in paths:
                #     if p is -1:
                #         continue
                #     print("new path:")
                #     for v in p:
                #         print(v.__str__())


    ###############################
    # def print_env(self):
    #     print_info("TIME IS: " + str(self.env_time))
    #
    #     print_info("OUR VERTICES TYPES:")
    #     v_types = []
    #     for vertex in self.graph.vertices:
    #         v_types.append(vertex.v_type)
    #     print_info(str(v_types))
    #
    #     print_info("OUR VERTICES PEOPLE COUNT: ")
    #     people_arr = self.graph.get_people_array_with_shelter()
    #     print_info(str(people_arr))
    #
    #     ppl_saved = sum([v.ppl_count for v in self.graph.vertices if v.is_shelter()])
    #     print_info("PEOPLE SAVED: " + str(ppl_saved) + "/" + str(self.total_ppl))
    ###############################