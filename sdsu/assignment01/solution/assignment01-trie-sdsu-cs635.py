#!/usr/bin/env python2

# Author: Vahid Pazirandeh (vpaziran@gmail.com)
#   Date: January 2013
#   Desc: Implementation of a map/dict interface using a trie
#         (tree data structure).
#         Assignment #1 for CS635 at SDSU, Spring 2013

# Note: Technically this implementation does not adhere to the required
# specifications of the original problem.


class Node:
    """
    What is this used for?
    Doc string missing. I also filled in other docstrings for you.
    """
    def __init__(self, key, value, value_node):
        self.key = key
        self.value = value

        # True if actual value node (typically leaf), otherwise
        # false (intermediary/inner node). Having an explicit
        # flag for value nodes allows nodes to contain values
        # like None (rather than having None have the meaning
        # of "non-value node").
        self.value_node = value_node

        # List of child Node references.        
        self.children = []

    def is_value_node(self):
        """
        Checks to see if this node is a value node
        """        
        return self.value_node

    def get_child(self, key):
        """
        Gets a child by key. If child with key does not exist, returns None
        """
        for child in self.children:
            if child.key == key:
                return child
        return None        

    def add_child(self, new_node):
        """
        Adds a child to this node
        """
        self.children.append(new_node)

    def __str__(self):
        return 'key={}, value={}, valueNode={}, numChildren={}'.format(
            self.key, self.value, self.value_node, len(self.children))

    @classmethod
    def new_value_node(cls, key, val):
        """
        Factory method for producing a new value node
        """
        return cls(key, val, True)
    # TODO: Not sure how to create static factory methods in Python,
    # but it would be nice to make the constructor private and have:
    #   newValueNode(key, val)
    #   newInnerNode(key)
    #   newEmptyNode()
    # Seems like a more intuitive interface.


# Implementation of a map interface using a Trie data structure.
#
# Note: Does not support insertion of entries with value None
# (i.e., no null values allowed).
class Trie:
    def __init__(self):
        self._rootNode = Node(key=None, value=None, valueNode=False)

    # Retrieve value associated with specified key. If not found,
    # returns None.
    def get(self, key):
        node = self._rootNode

        # Loop through all chars in key. If any node in the lineage
        # does not exist, then key must not exist in this tree.
        for char in key:
            child = node.getChild(char)
            if child:
                # Exists. Walk the tree by going down the descendants.
                node = child
            else:
                return None

        if node.isValueNode():
            return node.getValue()
        else:
            return None

    # Returns True if value exists in this trie, else False.
    def containsValue(self, value):
        # TODO: This can be more space and time efficient by returning
        # the first instance of value in the trie.
        return value in self.values()

    # Returns True if key exists in this trie, else False.
    def containsKey(self, key):
        return self.get(key) is not None

    # Add new key/value pair entry to this trie.
    def put(self, key, value):
        if not key or not value:
            raise Exception

        node = self._rootNode

        # Go through all but the last character in the new node's
        # key to be added. For each, add inner nodes as needed,
        # and walk down the tree until the parent of the new node
        # to be added is reached.
        for char in key[:-1]:
            child = node.getChild(char)
            if not child:
                # Child node not found. Create the inner child node
                # and visit it.
                newChild = Node(key=char, value=None, valueNode=False)
                node.addChild(newChild)
                node = newChild
            else:
                # The node with key=char exists. Walk down the tree
                # by visiting the node.
                node = child

        # Now process the last char in the node's key to be added. All
        # ancestors are guaranteed to have been created by this time.
        char = key[-1]
        child = node.getChild(char)
        if not child:
            # Most typical case: node with required key does not exist. Add it.
            node.addChild(Node(key=char, value=value, valueNode=True))
        else:
            # Node with key=char already exists; no need to add it. Just
            # make sure it is marked as a value node (inner node may be
            # promoted to value node here) and set the value.
            if not child.isValueNode():
                child.setValueNode(True)
                child.setValue(value)
            else:
                raise KeyError(
                    'Entry with key "{}" already exists'.format(key))

    # Iterate through all value nodes of the trie. This iterator is
    # implemented as a recursive generator. I love Python. :-)
    def __iter__(self, node=None):
        if not node:
            node = self._rootNode
        if node.isValueNode():
            yield node.getValue()
        for childNode in node.getChildren():
            for item in self.__iter__(childNode):
                yield item

    def values(self):
        return [item for item in self]

    # Return list of all values in this trie where each contains at
    # least a portion of the specified substring.
    def valuesContaining(self, substring):
        return filter(lambda s: substring in s, self.values())


def main():
    trie = Trie()

    goodKey = 'keyTwo'
    goodVal = 'dog'
    d = {'keyOne': 'attack', goodKey: goodVal, 'keyThree': 'cake', 'key': 'value'}

    print 'Adding the following key/value pairs to the trie:\n  {}'.format(d)
    for key, val in d.iteritems():
        trie.put(key, val)

    print ''
    partialVal = 'ck'
    print 'Find all words contaning "{}": {}'.format(partialVal, trie.valuesContaining(partialVal))
    print 'Find word associated with key="{}": {}'.format(goodKey, trie.get(goodKey))
    badKey = 'oops'
    badVal = 'frog'
    print 'Does the word "{}" exist? => {}'.format(badVal, trie.containsValue(badVal))
    print 'Does the word "{}" exist? => {}'.format(goodVal, trie.containsValue(goodVal))
    print 'Does an entry with the key "{}" exist? => {}'.format(badKey, trie.containsKey(badKey))
    print 'Does an entry with the key "{}" exist? => {}'.format(goodKey, trie.containsKey(goodKey))

    print ''
    print 'Print all words in trie: {}'.format(trie.values())


if __name__ == '__main__':
    main()

# EOF
