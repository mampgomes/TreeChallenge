class Tree:
    '''criacao de node
    @param self node actual
    @param val id da categoria a adicionar
    @param nome nome da categoria a adicionar'''
    def __init__(self, val, nome):
        self.val = val
        self.nome = nome
        self.nodes = []

    '''procura node pai (root caso nao especificado) e cria node filho
    caso node pai nao exista adiciona a root
    @param self node actual
    @param val id da categoria a adicionar
    @param nome nome da categoria a adicionar
    @node_ID id da categoria pai'''
    def add_node(self, val, nome, node_ID = 0):
        self.find_node(node_ID).nodes.append(Tree(val, nome))

    '''compara valor dado com o dos nodes filhos ate encontrar o node a remover
    testa os valores dos nodes filhos
    desce de profundidade quando nao encontra na actual
    @param self node actual   @param val id da categoria a adicionar
    @return node pai caso removido ou root caso contrario'''
    def remove_node(self, val):
        queue = [self]
        
        for cat in queue:
            for testing in cat.nodes:
                if val == testing.val:
                    cat.nodes.remove(testing)
                    return cat
            queue.extend(cat.nodes)
        return self
    
    '''procura node dando prioridade aos nodes do mesmo nivel (aka leitura horizontal)
    procura nos filhos dos nodes e caso nao encontre
    adiciona nodes do proximo nivel a queue
    @param self node actual
    @param val id da categoria a adicionar    
    @return node caso encontrado ou root caso contrario'''        
    def find_node(self, val):
        queue = []
        if self.val == 0:
            queue.extend(self.nodes)

        for cat in queue:
            if cat.val == val:
                return cat
            else:
                queue.extend(cat.nodes)
        return self
    
    '''representacao do node em string
    @param self node actual
    @return string formatada'''
    def __repr__(self):
        return "(%s)%s : {%s}" % (self.val, self.nome, self.nodes)


a = Tree(0, "root")
a.add_node(1, "cat1")
a.add_node(2, "cat2")
a.add_node(3, "cat3")
a.nodes[2].add_node(4, "cat4")
print(a)
a.add_node(5, "cat5", 4)
print(a)
a.remove_node(5)
print(a)
a.add_node(6,"cat6", 2)
a.add_node(7,"cat7", 4)
print(a)
a.remove_node(2)
a.remove_node(3)
print(a)
a.add_node(2, "cat2", 3)
a.remove_node(3)
print(a.find_node(2))
print(a)
