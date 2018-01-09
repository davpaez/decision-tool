import abc
import uuid

class Tree:
    def __init__(self):
        self.nodes = set()
        self.spaces = set()

    def add_node(self, node):
        self.nodes.add(node)

    def add_space(self, space):
        self.spaces.add(space)


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


class Space(metaclass=abc.ABCMeta):
    """Discrete space that follows a node.

    Options are abstract concepts that do not point to a concrete node

    TODO: Implement also the functionality for this class to work as a continuous space.
    """ 

    def __init__(self, tree, label):
        self.label = label
        self.options_labels = []
        self.parent_nodes = set()

        tree.add_space(self)

    def __repr__(self):
        return str('--[{}]--'.format(self.label))

    
    def add_option(self, option_label):
        """Adds an option"""
        self.options_labels.append(option_label)

    def add_parent_node(self, parent_node):
        self.parent_nodes.add(parent_node)

    def build_child_nodes(self, tree):
        child_nodes = []

        for i, option in enumerate(self.options_labels):
            n = Node(tree)
            n.parent_space = self
            n.option_id = i
            child_nodes.append(n)

        return child_nodes

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

children = pais.build_child_nodes(tree)
italia = children[0]
edimburgo = children[1]

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