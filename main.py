class TaskTCS(object):
    def __init__(self, input, output):
        self.error = False
        self.e1 = ''
        self.e2 = self.e4 = self.e5 = self.e6 = False
        self.isComplete = True
        self.e3 = ''
        self.fin = open(input)
        self.fout = open(output, 'w')
        for i in range(5):
            try:
                command = self.fin.readline()
                index1 = command.find('[')
                index2 = command.find(']')
                commandNew = command[index1 + 1: index2]
                if i == 0:
                    self.states = commandNew.split(",")
                    self.n = len(self.states)
                    if command.find("states=[") == -1 or index2 == -1:
                        self.e5 = True
                        self.error = True
                elif i == 1:
                    self.alpha = commandNew.split(",")
                    if command.find("alpha=[") == -1 or index2 == -1:
                        self.e5 = True
                        self.error = True
                elif i == 2:
                    self.initState = commandNew.split(",")
                    if command.find("initial=[") == -1 or index2 == -1:
                        self.e5 = True
                        self.error = True
                elif i == 3:
                    self.finState = commandNew.split(",")
                    if command.find("accepting=[") == -1 or index2 == -1:
                        self.e5 = True
                        self.error = True
                elif i == 4:
                    self.trans = commandNew.split(",")
                    if command.find("trans=[") == -1 or index2 == -1:
                        self.e5 = True
                        self.error = True
            except Exception:
                self.e5 = True
                self.error = True

    def dfs(self, start, g, visited, prev):
        visited[start] = True
        for u in g[start]:
            if not visited[u]:
                prev[u] = start
                self.dfs(u, g, visited, prev)

    def isError(self):
        return self.error

    def printErrors(self):
        if self.e1 != '':

            f = open('output.txt', 'w')

            f.write('Error:' + '\n' + "E1: A state '" + self.e1 + "' is not in the set of states")

            f.close()

        elif self.e2:

            f = open('output.txt', 'w')

            f.write('Error:' + '\n' + 'E2: Some states are disjoint')

            f.close()

        elif self.e3 != '':

            f = open('output.txt', 'w')

            f.write('Error:' + '\n' + "E3: A transition '" + self.e3 + "' is not represented in the alphabet")

            f.close()

        elif self.e4:

            f = open('output.txt', 'w')

            f.write('Error:' + '\n' + 'E4: Initial state is not defined')

            f.close()

        elif self.e5:

            f = open('output.txt', 'w')

            f.write('Error:' + '\n' + 'E0: Input file is malformed')

            f.close()

        elif self.e6:

            f = open('output.txt', 'w')

            f.write('Error:' + '\n' + 'E5: FSA is nondeterministic')

            f.close()

    def check(self):

        visited = [False] * self.n

        prev = [None] * self.n

        # a graph that checks whether every state has all "alpha"

        gAlp = [[] for i in range(self.n)]

        # graph of transitions (non-directed)

        g = [[] for i in range(self.n)]

        # directed graph of transitions

        gDirected = [[] for i in range(self.n)]

        g1 = [0] * self.n

        # E4 error
        if self.initState[0] == '':

            self.e4 = True

            self.error = True

        # E1 error
        if self.initState[0] not in self.states:

            self.e1 = self.initState[0]

            self.error = True

        transitions = [[] for i in range(len(self.states))]

        if not self.error:

            for i in self.trans:

                # go through list of transitions and check

                # whether s1, s2 are in states and a is in alpha

                s1, a, s2 = i.split('>')

                transitions[self.states.index(s1)].append(a)

                if s1 not in self.states:

                    self.e1 = s1

                    self.error = True

                    break
                ind1 = self.states.index(s1)

                if s2 not in self.states:
                    self.e1 = s2
                    self.error = True
                    break
                ind2 = self.states.index(s2)
                if ind2 not in gDirected[ind1]:
                    gDirected[ind1].append(ind2)
                if a not in gAlp[ind1]:
                    gAlp[ind1].append(a)
                if ind2 != ind1:
                    if ind2 not in g[ind1]:
                        g[ind1].append(ind2)
                    if ind1 not in g[ind2]:
                        g[ind2].append(ind1)
                if s1 not in self.states:
                    self.error = True
                    g1[ind1] += 1
                    self.e1 = s1
                    break
                elif s2 not in self.states:
                    self.error = True
                    self.e1 = s2
                    break
                elif a not in self.alpha:
                    self.error = True
                    self.e3 = a
                    break

        for tr in transitions:
            for i in self.trans:
                s1, a, s2 = i.split('>')
                if a in tr and tr.count(a) == 1 or a not in tr:
                    pass
                else:
                    self.e6 = True
                    self.error = True

        # isComplete
        for i in range(self.n):
            if len(gAlp[i]) != len(self.alpha):
                self.isComplete = False

        # checking the graph for connectivity

        self.dfs(0, g, visited, prev)
        if False in visited:
            self.error = True
            self.e2 = True





    def toRegExp(self):
        fin_states_ind = []
        init_ind = 0
        r = self._get_init_regex(fin_states_ind, init_ind)
        for k in range(len(self.states)):
            new_r = [[0] * len(self.states) for i in range(len(self.states))]
            for i in range(len(self.states)):
                for j in range(len(self.states)):
                    new_r[i][j] = "(" + r[i][k] + ")(" + r[k][k] + ")*(" + r[k][j] + ")|(" + r[i][j] + ")"
            r = new_r

        result = ''
        for j in fin_states_ind:
            result += r[init_ind][j] + "|"

        f = open('output.txt', 'w')

        if result == '':
            f.write("{}")
        else:
            f.write(result[0:-1])
        f.close()
    def _get_init_regex(self, fin_states_ind, init_ind):
        init_regex = [[''] * len(self.states) for i in range(len(self.states))]

        for i in range(len(self.states)):
            state = self.states[i]
            if state in self.finState:
                fin_states_ind.append(i)

        for i in range(len(self.states)):
            state = self.states[i]

            if state in self.initState:
                init_ind = i

            for j in range(len(self.states)):
                new_state = self.states[j]
                regex = ''

                for transition in self.trans:  # in state.trans
                    trans_info = transition.split('>')
                    if trans_info[2] == new_state and trans_info[0] == state:
                        regex += trans_info[1] + "|"
                if state == new_state:
                    regex += "eps"
                if regex == '':
                    regex = "{}"
                if regex[-1] == "|":
                    regex = regex[0:-1]
                init_regex[i][j] = regex
        return init_regex




validator = TaskTCS('input.txt', 'output.txt')

validator.check()

if validator.isError():

    validator.printErrors()

else:

    validator.toRegExp()
