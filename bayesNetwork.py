import copy


class bayesNetwork:
    def __init__(self, env_graph):
        self.env_graph = env_graph
        self.networkObjects = []
        self.buildNetworkFromGraph()
        self.buildNetworkFromGraph(time=1)
        self.printGraph()

    class node:
        def __init__(self, n_type, index, time, probabilityTable, parents, children, weight=None):
            self.probabilityTable = probabilityTable
            self.n_type = n_type
            self.index = index
            self.time = time
            self.parents = parents
            self.children = children
            self.weight = weight  # Relevant only for Edge node

        def __eq__(self, other):
            if isinstance(other, bayesNetwork.node):
                return other.n_type is self.n_type and other.index == self.index and other.time == self.time
            return False

    class VarWithVal:
        def __init__(self, variable, value):
            """
            :type variable: bayesNetwork.node
            """
            self.variable = variable
            self.value = value

    def buildNetworkFromGraph(self, time=0):
        for city in self.env_graph.vertices:
            newCity = self.node("V", city.index, time, None, [], [])
            if time is not 0:
                newCity.parents.append(self.getBayesNode("V", city.index, time-1))
                self.getBayesNode("V", city.index, time - 1).children.append(newCity)
            self.networkObjects.append(newCity)

        for edge in self.env_graph.edges:
            v1 = edge.vertex_1
            v2 = edge.vertex_2
            newEdge = self.node("E", edge.index, time, None, [], [], 3)
            newEdge.parents.append(self.getBayesNode("V", v1.index, time))
            newEdge.parents.append(self.getBayesNode("V", v2.index, time))
            self.networkObjects.append(newEdge)

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
        ev_1 = copy.copy(evidence).append(x_true)
        ev_2 = copy.copy(evidence).append(x_false)

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
        for e in evidence:
            if e.variable == y:
                y_has_value_in_evidence = True
                break
        if y_has_value_in_evidence:
            pass  # TODO

    def getBayesNode(self, n_type, index, time=0):
        for node in self.networkObjects:
            if node.n_type is n_type and node.index is index and node.time is time:
                return node
        return -1

    def getVars(self):
        return self.networkObjects

    def printGraph(self):
        pass  # TODO






