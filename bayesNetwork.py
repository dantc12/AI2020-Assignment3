import copy
from helper_funcs import print_info
from decimal import *


class bayesNetwork:
    def __init__(self, env_graph):
        """
        :type env_graph: graph.Graph
        """
        self.env_graph = env_graph
        self.networkObjects = []  # type: list[bayesNetwork.node]
        self.buildNetworkFromGraph()
        self.buildNetworkFromGraph(time=1)
        self.printGraph()

    class node:
        def __init__(self, n_type, index, time, parents, children, weight=None):
            """
            :type children: list[bayesNetwork.node]
            :type parents: list[bayesNetwork.node]
            :type n_type: str
            """
            self.n_type = n_type
            self.index = index
            self.time = time
            self.parents = parents
            self.children = children
            self.weight = weight  # Relevant only for Edge node

            self.probabilityTable = {}

        # Probabilites: [p(T)] (no parents), [F, T] (1 parent), [FF, FT, TF, TT] (2 parents)
        def fillProbabilityTable(self, probabilities):
            if not self.parents:
                self.probabilityTable['1'] = round(probabilities[0], 5)
            else:
                permutations = list(self.perms(len(self.parents)))
                i = 0
                for perm in permutations:
                    self.probabilityTable[str(perm)] = round(probabilities[i], 5)
                    i += 1

        def varValFromEvidence(self, evidence_list):
            """
            :type evidence_list: list[bayesNetwork.VarWithVal]
            """
            for e in evidence_list:
                if e.variable == self:
                    return e.value
            return None

        def p_varValGivenParents(self, self_value, evidence_list):
            """
            :type self_value: bool
            :type evidence_list: list[bayesNetwork.VarWithVal]
            """
            if not self.parents:
                self_true_val = self.probabilityTable['1']
            elif len(self.parents) == 1:
                parent1_bin_val = bin(self.parents[0].varValFromEvidence(evidence_list))[2:]
                self_true_val = self.probabilityTable[parent1_bin_val]
            else:  # 2 Parents
                parent1_bin_val = bin(self.parents[0].varValFromEvidence(evidence_list))[2:]
                parent2_bin_val = bin(self.parents[1].varValFromEvidence(evidence_list))[2:]
                self_true_val = self.probabilityTable[parent1_bin_val + parent2_bin_val]
            if self_value:  # Asked for self p(True) value
                return self_true_val
            else:
                return 1 - self_true_val

        @staticmethod
        def perms(n):
            if not n:
                return
            for i in list(range((2 ** n))):
                s = bin(i)[2:]
                s = "0" * (n - len(s)) + s
                yield s

        def printNodeInfo(self):
            if self.n_type == 'V':
                print_info("VERTEX " + str(self.index) + ", time " + str(self.time) + ":")
                if not self.parents:
                    print_info("\tP(Flooding = True) = " + str(self.probabilityTable['1']))
                    print_info("\tP(Flooding = False) = " + str(1 - self.probabilityTable['1']))
                elif len(self.parents) == 1:
                    print_info("\tP(Flooding = True | Flooding " + str(self.parents[0]) + " = True) = " +
                               str(self.probabilityTable['1']))
                    print_info("\tP(Flooding = False | Flooding " + str(self.parents[0]) + " = True) = " +
                               str(1 - self.probabilityTable['1']))
                    print_info("\tP(Flooding = True | Flooding " + str(self.parents[0]) + " = False) = " +
                               str(self.probabilityTable['0']))
                    print_info("\tP(Flooding = False | Flooding " + str(self.parents[0]) + " = False) = " +
                               str(1 - self.probabilityTable['0']))
            else:  # 2 Parents
                print_info("EDGE " + str(self.index) + ", time " + str(self.time) + ":")
                for pos_vals in [(True, True), (True, False), (False, True), (False, False)]:
                    print_info("\tP(Blockage = True | Flooding " + str(self.parents[0]) + " = " + str(pos_vals[0]) +
                               ", Flooding " + str(self.parents[1]) + " = " + str(pos_vals[1]) +
                               ") = " + str(self.probabilityTable[bin(pos_vals[0])[2:] + bin(pos_vals[1])[2:]]))

        def __str__(self):
            return str(self.n_type) + str(self.index) + str(self.time)

        def __lt__(self, other):
            if isinstance(other, bayesNetwork.node):
                if self.time != other.time:
                    return self.time < other.time
                else:
                    if self.n_type != other.n_type:
                        return self.n_type == 'V'
                    else:
                        return self.index < other.index
            raise Exception("Problem comparing nodes")

        def __le__(self, other):
            if isinstance(other, bayesNetwork.node):
                if self.time != other.time:
                    return self.time < other.time
                else:
                    if self.n_type != other.n_type:
                        return self.n_type == 'V'
                    else:
                        return self.index <= other.index

        def __eq__(self, other):
            if isinstance(other, bayesNetwork.node):
                return other.n_type is self.n_type and other.index == self.index and other.time == self.time
            return False

    # A class for nodes that are assigned value. Used for evidence and queries.
    class VarWithVal:
        def __init__(self, variable, value):
            """
            :type variable: bayesNetwork.node
            """
            self.variable = variable
            self.value = value

        def __str__(self):
            return "(" + str(self.variable) + ", " + str(self.value) + ")"

    def buildNetworkFromGraph(self, time=0):
        p_persistence = self.env_graph.p_persistence
        p_leakage = self.env_graph.p_leakage
        for city in self.env_graph.vertices:
            newCity = self.node("V", city.index, time, [], [])
            if time == 0:
                newCity.fillProbabilityTable([city.pv])  # [p(T)] (no parents)
            else:
                parentCityNode = self.getBayesNode("V", city.index, time-1)
                newCity.parents.append(parentCityNode)
                newCity.fillProbabilityTable([city.pv, p_persistence])  # [F, T] (1 parent)
                self.getBayesNode("V", city.index, time - 1).children.append(newCity)
            self.networkObjects.append(newCity)

        for edge in self.env_graph.edges:
            v1 = edge.vertex_1
            v2 = edge.vertex_2
            newEdge = self.node("E", edge.index, time, [], [], 3)
            newEdge.parents.append(self.getBayesNode("V", v1.index, time))
            newEdge.parents.append(self.getBayesNode("V", v2.index, time))

            q_i = 1 - 0.6 * (1 / float(edge.weight))
            # newEdge.fillProbabilityTable([p_leakage, Decimal(1 - q_i).quantize(Decimal('.0001')), \
            # Decimal(1 - q_i).quantize(Decimal('.0001')), Decimal(1 - (q_i*q_i)).quantize(Decimal('.0001'))])  \
            # [FF, FT, TF, TT] (2 parents)
            newEdge.fillProbabilityTable([p_leakage, 1 - q_i, 1 - q_i, 1 - (q_i*q_i)])  # [FF, FT, TF, TT] (2 parents)
            self.networkObjects.append(newEdge)

    def sort_network_objects(self):
        """
        Run a topological sort to determine the order of the variables.
        All parents of a node has to be added before the node is added, and ties
        are broken alphabetically.
        """
        self.networkObjects.sort()

    def enumerate_ask(self, query, evidence):
        """
        :type evidence: list[bayesNetwork.VarWithVal]
        :type query: bayesNetwork.node
        """
        res_prob_table = [0.0, 0.0]

        # For each value of query var
        x_true = self.VarWithVal(query, True)
        x_false = self.VarWithVal(query, False)

        # Extending evidence with possible var value
        ev_1 = copy.copy(evidence)
        ev_2 = copy.copy(evidence)
        ev_1.append(x_true)
        ev_2.append(x_false)

        # Sorting variables first
        self.sort_network_objects()

        #  Given the evidence the probability of this specific evidence is 1 or 0
        for ev in evidence:
            if str(ev.variable) == str(x_true.variable):
                if ev.value is True:
                    res_prob_table[0] = 1
                    res_prob_table[1] = 0
                else:
                    res_prob_table[0] = 0
                    res_prob_table[1] = 1
                return res_prob_table

        # Choosing the relevant nodes
        relevant_vars = []
        tmp_n_queue = [query]
        while tmp_n_queue:
            tmp_n = tmp_n_queue[0]
            relevant_vars = tmp_n.parents + relevant_vars
            tmp_n_queue += tmp_n.parents
            tmp_n_queue.remove(tmp_n_queue[0])
        relevant_vars += [query]
        tmp_n_queue = [query]
        while tmp_n_queue:
            tmp_n = tmp_n_queue[0]
            relevant_vars += tmp_n.children
            tmp_n_queue += tmp_n.children
            tmp_n_queue.remove(tmp_n_queue[0])
        relevant_vars.sort()
        # relevant_vars = query.parents + [query] + query.children
        # relevant_vars = self.getVars()

        # Results coming in for each option of query var
        res_prob_table[0] = self.enumerate_all(relevant_vars, ev_1)  # True
        res_prob_table[1] = self.enumerate_all(relevant_vars, ev_2)  # False

        # Normalising
        norm_scale = sum(res_prob_table)
        if norm_scale != 0:
            res_prob_table[0] = res_prob_table[0] / norm_scale
            res_prob_table[1] = res_prob_table[1] / norm_scale

        return res_prob_table

    @staticmethod
    def enumerate_all(variables, evidence_list):
        """
        Variables come sorted!
        :type evidence_list: list[bayesNetwork.VarWithVal]
        :type variables: list[bayesNetwork.node]
        """
        if not variables:
            return 1.0
        y = variables[0]
        y_val = y.varValFromEvidence(evidence_list)
        if y_val is not None:
            y_p_givenParents_val = y.p_varValGivenParents(y_val, evidence_list)
            return y_p_givenParents_val * bayesNetwork.enumerate_all(variables[1:], evidence_list)
        else:
            # Extending evidence with possible y value
            ev_y_true = copy.copy(evidence_list)
            ev_y_false = copy.copy(evidence_list)
            ev_y_true.append(bayesNetwork.VarWithVal(y, True))
            ev_y_false.append(bayesNetwork.VarWithVal(y, False))

            y_true_p_givenParents_val = y.p_varValGivenParents(True, evidence_list)
            y_false_p_givenParents_val = y.p_varValGivenParents(False, evidence_list)

            return ((y_true_p_givenParents_val * bayesNetwork.enumerate_all(variables[1:], ev_y_true)) +
                    (y_false_p_givenParents_val * bayesNetwork.enumerate_all(variables[1:], ev_y_false)))

    def query_floodings(self, evidence_list):
        print_info("Printing probability that each of the vertices is flooded:")
        flood_nodes = [n for n in self.networkObjects if n.n_type == 'V']
        for fl_node in flood_nodes:
            flood_chances = self.enumerate_ask(fl_node, evidence_list)
            print_info("\tP(" + str(fl_node) + " Flooding = True) = " + str(flood_chances[0]))

    def query_blockages(self, evidence_list):
        print_info("Printing probability that each of the edges is blocked:")
        blockage_nodes = [n for n in self.networkObjects if n.n_type == 'E']
        for bl_node in blockage_nodes:
            blockage_chances = self.enumerate_ask(bl_node, evidence_list)
            print_info("\tP(" + str(bl_node) + " Blockage = True) = " + str(blockage_chances[0]))

    def query_pathNotBlocked(self, path, evidence_list):
        # finalProb = 1
        ev_list = copy.copy(evidence_list)
        v1, v2 = self.getEdgeVertexesVariables(path[0])
        finalProb = self.enumerate_ask(v1, ev_list)[1]
        ev_list.append(self.VarWithVal(v1, False))

        for edge in path:
            v1, v2 = self.getEdgeVertexesVariables(edge)
            finalProb = finalProb * self.enumerate_ask(edge, ev_list)[1]
            ev_list.append(self.VarWithVal(edge, False))
            # val = self.enumerate_ask(v2, evidence_list)[1]
            finalProb = finalProb * self.enumerate_ask(v2, ev_list)[1]
            ev_list.append(self.VarWithVal(v2, False))

        return finalProb

    def getBayesNode(self, n_type, index, time=0):
        for node in self.networkObjects:
            if node.n_type is n_type and node.index is index and node.time is time:
                return node
        return -1

    def getVars(self):
        return self.networkObjects

    def printGraph(self):
        self.sort_network_objects()
        for n in self.networkObjects:
            n.printNodeInfo()
            # more TODO here

    def getBayesNodeByName(self, varName):
        for var in self.networkObjects:
            varStr = str(var)
            if varStr == varName:
                return var
        raise Exception("No such edge " + varName)

    def getEdgeVertexesVariables(self, edge_node):
        """
        :type edge_node: bayesNetwork.node
        """
        edgeNodeFullName = str(edge_node)
        edgeName = edgeNodeFullName[0:2]
        time = edge_node.time
        edgeInGraph = self.env_graph.get_edge_from_string(edgeName)
        v1 = edgeInGraph.vertex_1
        v2 = edgeInGraph.vertex_2
        v1Node = self.getBayesNodeByName(str(v1) + str(time))
        v2Node = self.getBayesNodeByName(str(v2) + str(time))

        return v1Node, v2Node
