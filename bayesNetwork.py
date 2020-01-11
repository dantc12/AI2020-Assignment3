import copy


class bayesNetwork:
    def __init__(self, env_graph):
        """
        :type env_graph: graph.Graph
        """
        self.env_graph = env_graph
        self.networkObjects = []
        self.buildNetworkFromGraph()
        self.buildNetworkFromGraph(time=1)
        self.printGraph()

    class node:
        def __init__(self, n_type, index, time, parents, children, weight=None):
            """
            :type children: list[node]
            :type parents: list[node]
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
                self.probabilityTable['1'] = probabilities[0]
            else:
                permutations = list(self.perms(len(self.parents)))
                i = 0
                for perm in permutations:
                    self.probabilityTable[str(perm)] = str(probabilities[i])
                    i += 1

        @staticmethod
        def perms(n):
            if not n:
                return
            for i in list(range((2 ** n))):
                s = bin(i)[2:]
                s = "0" * (n - len(s)) + s
                yield s

        def __str__(self):
            return str(self.n_type) + str(self.index) + str(self.time)

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
            newEdge = self.node("E", edge.index, time, None, [], [], 3)
            newEdge.parents.append(self.getBayesNode("V", v1.index, time))
            newEdge.parents.append(self.getBayesNode("V", v2.index, time))

            q_i = 1 - 0.6 * (1 / float(edge.weight))
            newEdge.fillProbabilityTable([p_leakage, 1 - q_i, 1 - q_i, 1 - (q_i*q_i)])  # [FF, FT, TF, TT] (2 parents)
            self.networkObjects.append(newEdge)

    # Assuming this is called with variables ordered
    def enumerate_ask(self, query, evidence):
        """
        :type evidence: list[VarWithVal]
        :type query: VarWithVal
        """
        res_prob_table = [0.0, 0.0]

        # For each value of query var
        x_true = self.VarWithVal(query.variable, True)
        x_false = self.VarWithVal(query.variable, False)

        # Extending evidence with possible var value
        ev_1 = copy.copy(evidence)
        ev_2 = copy.copy(evidence)
        ev_1.append(x_true)
        ev_2.append(x_false)

        # Results coming in for each option of query var
        res_prob_table[0] = self.enumerate_all(self.getVars(), ev_1)
        res_prob_table[1] = self.enumerate_all(self.getVars(), ev_2)

        # Normalising
        norm_scale = sum(res_prob_table)
        res_prob_table[0] = res_prob_table[0] / norm_scale
        res_prob_table[1] = res_prob_table[1] / norm_scale

        return res_prob_table

    @staticmethod
    def enumerate_all(vars, evidence):
        """
        :type evidence: list[bayesNetwork.VarWithVal]
        :type vars: list[bayesNetwork.node]
        """
        if not vars:
            return 1.0
        y = vars[0]
        y_has_value_in_evidence = False
        y_with_val = None
        for e in evidence:
            if e.variable == y:
                y_has_value_in_evidence = True
                y_with_val = e
                break
        if y_has_value_in_evidence:
            p_y_given_parents = 0.0
            if y_with_val.value == True:
                p_y_given_parents = y.probabilityTable  # TODO

    def getBayesNode(self, n_type, index, time=0):
        for node in self.networkObjects:
            if node.n_type is n_type and node.index is index and node.time is time:
                return node
        return -1

    def getVars(self):
        return self.networkObjects

    def printGraph(self):
        pass  # TODO






