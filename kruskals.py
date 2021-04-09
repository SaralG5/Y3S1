# implement union find data structure
class DisjointSet:
    def __init__(self, vertex_number):
        self.vertex_parent = []  # initialise an array to hold the id and parent values.
        for k in range(vertex_number):  # put the height and vertex id's into the array
            self.vertex_parent.append([k, -1])

    def find(self, vertex):
        if self.vertex_parent[vertex][1] < 0: # its its own parent
            return vertex
        else: # reset all the children to the root
            self.vertex_parent[vertex][1] = self.find(self.vertex_parent[vertex][1])
            return self.vertex_parent[vertex][1]

    def union(self, u, v):
        root_u = self.find(u)  # get the root of vertex u
        root_v = self.find(v)
        if root_u == root_v:   # u and v already in same tree se we don't need to worry.
            return
        height_u = -self.vertex_parent[u][1]
        height_v = -self.vertex_parent[v][1]
        if height_u > height_v: # the height of the 'u' tree is bigger
            # here we set the parent of v to be u
            self.vertex_parent[v][1] = root_u
        elif height_v > height_u:  # the height of the 'v' tree is bigger
            # here we set the parent of u to be v.
            self.vertex_parent[u][1] = root_v
        else:  # here the height of the two trees are equal
            self.vertex_parent[u][1] = root_v
            self.vertex_parent[v][1] = -(height_u + 1)
