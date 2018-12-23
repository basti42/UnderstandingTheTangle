# -*- coding: utf-8 -*-

import hashlib

class Transaction:

    def __init__(self, frm, to, amount):
        """
        Class describing a Transaction to be passed to a TangleNode
        as a parameter.
        :param  frm, to : str   sender and recipient of the transaction
        :param  amount  : float amount to be transfered
        """
        self.sender = frm
        self.recipient = to
        self.amount = amount
        self.hash = self.__sha256StringHash__(bytes(frm+to+str(amount), "utf-8"))

    def __sha256StringHash__(self, string):
        """
        Making a hash (sha256) from concatenated sender, recipient and amount
        """
        m = hashlib.sha256()
        m.update(string)
        return m.hexdigest()

    def __repr__(self):
        return "From: " + str(self.sender) + ", To: " + str(self.recipient) + ", Amount: " + str(self.amount)


class TangleNode:

    def __init__(self, transaction):
        """
        A Node in the directed, acyclic graph. Payoad of a node is
        an object of type Transaction.
        :param  transaction :   Transaction
        """
        self.payload = transaction
        self.isValidated = False
        self.validationCount = 0
        self.validationThreshold = 4
        self.firstValidationNode = None
        self.secondValidationNode = None

    def setValidationNodes(self, first, second):
        """
        set the pointer to the nodes to be validated by
        this node. Nodes are chosen by the graph.
        :param  first, second   :   TangleNode
        """
        self.firstValidationNode = first
        self.secondValidationNode = second

    def validateNodes(self):
        """
        calculate the hash of each of the nodes pointed to and compare
        to the original has stored in them. If they match, increment
        their validationCount. Setting their validity is done by the graph,
        which choses the nodes
        """
        firststring = self.firstValidationNode.payload.sender + self.firstValidationNode.payload.recipient + str(self.firstValidationNode.payload.amount)
        firsthash = self.firstValidationNode.payload.__sha256StringHash__(bytes(firststring, "utf-8"))
        if (firsthash == self.firstValidationNode.payload.hash):
            self.firstValidationNode.validationCount += 1
        else:
            print("[WRONG HASH]" + self.firstValidationNode)

        secondstring = self.secondValidationNode.payload.sender + self.secondValidationNode.payload.recipient + str(self.secondValidationNode.payload.amount)
        secondhash = self.secondValidationNode.payload.__sha256StringHash__(bytes(secondstring, "utf-8"))
        if (secondhash == self.secondValidationNode.payload.hash):
            self.secondValidationNode.validationCount += 1
        else:
            print("[WRONG HASH]" + self.secondValidationNode)


    def __repr__(self):
        return "[Node Payload]: " + str(self.payload) + " [Node Valid]: " + str(self.isValidated)
