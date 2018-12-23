# -*- coding: utf-8 -*-

import numpy as np
from TangleNode import Transaction, TangleNode

class Tangle:

    def __init__(self):
        """
        A directed, acyclic graph, keeping track of the nodes
        and taking care of validation and transactions
        """
        self.genesisTransaction = Transaction("Everyone", "", 1000)
        self.genesis = TangleNode(self.genesisTransaction)
        self.totalNumberOfNodes = 1      # count the number of nodes in the DAG
        self.nodes = [self.genesis]      # keeps track of nodes, that are not validated yet
        self.validatedNodes = []

    def addNode(self, transaction):
        """
        Creates a new TangleNode from a given Transaction
        to be added to the DAG, before adding this node to
        the non-valid nodes list, give it two other nodes
        to check their hashes.
        """
        newNode = TangleNode(transaction)

        if len(self.nodes) >= 2: # there are enough nodes to collect two
            oneIdx = np.random.choice(np.arange(0,len(self.nodes)))
            twoIdx = oneIdx
            while twoIdx == oneIdx:
                twoIdx = np.random.choice(np.arange(0,len(self.nodes)))
            assert oneIdx != twoIdx, "same index for chosing nodes to validate!"

            one = self.nodes.pop(oneIdx)
            two = self.nodes.pop(twoIdx-1)  # due to the first pop the index reduces

            newNode.setValidationNodes(one, two)
            newNode.validateNodes()

            if one.validationCount >= one.validationThreshold: one.isValidated = True
            if two.validationCount >= two.validationThreshold: two.isValidated = True

            # check if these selected nodes are now validated
            if one.isValidated:
                self.validatedNodes.append(one)
            else:
                self.nodes.append(one)

            if two.isValidated:
                self.validatedNodes.append(two)
            else:
                self.nodes.append(two)

        # add the new node to the nodes list
        self.nodes.append(newNode)
        self.totalNumberOfNodes += 1

    def __repr__(self):
        return "[Total Nodes: {:4d} (Non-validated: {:4d} - Validated: {:4d})]".format(
            self.totalNumberOfNodes, len(self.nodes), len(self.validatedNodes)
        )
