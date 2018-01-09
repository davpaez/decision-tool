import abc
import uuid

class Tree:
    def __init__(self):
        self.nodes = []
        self.spaces = []

    def add_node(self, node):
        self.nodes.append(node)

    def add_space(self, space):
        self.spaces.append(space)


class Node:
    """Object representing a point of multifurcation in a decision tree.

    """
    def __init__(self, tree):
        self.id = uuid.uuid4()

        self.utility = 0
        self.prob = 0
        self.ev = 0

        self.parent_space = None
        self.option_id = None
        self.child_space = None

        self.child_nodes = []
        self.parent_node = None

        tree.add_node(self)

    
    def __repr__(self):
        return str('({})'.format(self.get_option_label()))

    def add_child_space(self, space):
        self.child_space = space
        space.add_parent_node(self)

    def get_option_label(self):
        if self.parent_space is None:
            return 'Root'
        else:
            return self.parent_space.options_labels[self.option_id]

    def add_child_node(self, node):
        self.child_nodes.append(node)

    def build_child_nodes(self, tree):
        if self.child_space is not None:
            child_nodes = []
            for i, option in enumerate(self.child_space.options_labels):
                n = Node(tree)
                n.parent_space = self.child_space
                n.option_id = i
                child_nodes.append(n)
            self.child_nodes = child_nodes


class Space(metaclass=abc.ABCMeta):
    """Discrete space that follows a node.

    Options are abstract concepts that do not point to a concrete node

    TODO: Implement also the functionality for this class to work as a continuous space.
    """ 

    def __init__(self, tree, label):
        self.label = label
        self.options_labels = []
        self.parent_nodes = []

        tree.add_space(self)

    def __repr__(self):
        return str('--[{}]--'.format(self.label))

    
    def add_option(self, option_label):
        """Adds an option"""
        self.options_labels.append(option_label)

    def add_parent_node(self, parent_node):
        self.parent_nodes.append(parent_node)

    def build_child_nodes(self, tree):
        for node in self.parent_nodes:
            node.build_child_nodes(tree)

    @abc.abstractmethod
    def example(self):
        """Do something"""

class ActionSpace(Space):
    """Discrete action space that follows a decision node.

    TODO: Implement also the functionality for this class to work as a continuous action space.
    """
    def __init__(self, tree, label):
        super(ActionSpace, self).__init__(tree, label)

    def example(self):
        pass



class ChanceSpace(Space):
    """Discrete space that follows a chance node.

    TODO: Implement also the functionality for this class to work as a continuous action space.
    """ 
    def __init__(self, tree, label):
        super(ChanceSpace, self).__init__(tree, label)
        self.options_prob = []

    def example(self):
        pass

    def add_option(self, option_label, option_prob):
        self.options_labels.append(option_label)
        self.options_prob.append(option_prob)



class SpaceFactory:
    
    constructors = {'action' : ActionSpace, 
                    'chance' : ChanceSpace}

    @classmethod
    def build(cls, tree, kind_name, label):
        return cls.constructors[kind_name](tree, label)



tree = Tree()

root = Node(tree)
pais = SpaceFactory.build(tree, 'action', 'Eleccion pais')
root.add_child_space(pais)


pais.add_option('Italia')
pais.add_option('Edimburgo')
pais.add_option('Colombia')

pais.build_child_nodes(tree)
italia = root.child_nodes[0]
edimburgo = root.child_nodes[1]

action2 = SpaceFactory.build(tree, 'action', 'TipoTrabajo')
action2.add_option('Independiente')
action2.add_option('Empleada')

chance1 = SpaceFactory.build(tree, 'chance', 'ActitudKiko')
chance1.add_option('Sigue problema', 0.7)
chance1.add_option('Para problema', 0.3)


italia.add_child_space(action2)
edimburgo.add_child_space(action2)

action2.build_child_nodes(tree)


print(tree.nodes)