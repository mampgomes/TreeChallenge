'''
@author: Marco André de Matos Pereira Gomes
@Date: 13/05/2021
'''
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
    def add_node(self, val, nome, dad = "root"):
        if(self.find_node(dad) == None):
            return None
        if(self.find_node(nome))!= None:
            return None
        self.find_node(dad).nodes.append(Tree(val, nome))
        return self

    '''compara valor dado com o dos nodes filhos ate encontrar o node a remover
    testa os valores dos nodes filhos
    desce de profundidade quando nao encontra na actual
    @param self node actual   @param val id da categoria a adicionar
    @return node pai caso removido ou root caso contrario'''
    def remove_node(self, name):
        queue = [self]
        
        for cat in queue:
            for testing in cat.nodes:
                if name == testing.nome:
                    cat.nodes.remove(testing)
                    return cat
            queue.extend(cat.nodes)
        return None
    
    '''procura node dando prioridade aos nodes do mesmo nivel (aka leitura horizontal)
    procura nos filhos dos nodes e caso nao encontre
    adiciona nodes do proximo nivel a queue
    @param self node actual
    @param val id da categoria a adicionar    
    @return node caso encontrado ou root caso contrario'''        
    def find_node(self, nome):
        queue = [self]

        for cat in queue:
            if cat.nome == nome:
                return cat
            else:
                queue.extend(cat.nodes)
        return None
    
    def printTable(self, nome = ''):
        flag = False
        if nome == '':
            flag = True
            nome ="root"
        table = self.find_node(nome)
        if(len(table.nodes) > 0):
            print("%s(%s):\n" %(table.nome, table.val))
            for record in table.nodes:
                print("\t%s" % (record.nome))
            if flag:
                for record in table.nodes:
                    self.printTable(record.nome)

    '''representacao do node em string
    @param self node actual
    @return string formatada'''
    def __repr__(self):
        return "(%s)%s\n\t%s" % (self.val, self.nome, self.nodes)

if __name__ == "__main__":
    a = Tree(0, "root")
    a.add_node(1, "cat1")
    a.add_node(1, "cat1")
    a.add_node(2, "cat2")
    a.add_node(3, "cat3")
    a.add_node(4, "cat4", "cat3")
    print(a)
    a.add_node(5, "cat5", "cat4")
    print(a)
    a.remove_node("cat5")
    print(a)
    a.add_node(6,"cat6", "cat2")
    a.add_node(7,"cat7", "cat4")
    print(a)
    a.remove_node("cat2")
    a.remove_node("cat3")
    print(a)
    a.add_node(2, "cat2", "cat3")
    a.remove_node("cat3")
    print(a.find_node("cat2"))
    print(a)
