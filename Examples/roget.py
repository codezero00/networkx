#!/usr/bin/env python
"""
The roget.dat example from the Stanford Graph Base.

Build a directed graph of 1022 categories and
5075 cross-references as defined in the 1879 version of Roget's Thesaurus
contained in the datafile roget.dat. This example is described in
Section 1.2 in Knuth's book [1,2].

Note that one of the 5075 cross references is a self loop and
thus is not included in the graph built here because 
the standard NX Graph class doesn't include self loops
(cf. 400pungency:400 401 403 405).

References.
----------

[1] Donald E. Knuth,
    "The Stanford GraphBase: A Platform for Combinatorial Computing",
    ACM Press, New York, 1993.
[2] http://www-cs-faculty.stanford.edu/~knuth/sgb.html


"""
__author__ = """Brendt Wohlberg\nAric Hagberg (hagberg@lanl.gov)"""
__date__ = "$Date: 2005-04-01 07:56:22 -0700 (Fri, 01 Apr 2005) $"
__credits__ = """"""
__revision__ = ""
#    Copyright (C) 2004 by 
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    Distributed under the terms of the GNU Lesser General Public License
#    http://www.gnu.org/copyleft/lesser.html

from NX import *
import re
import sys

def roget_graph():
    """ Return the thesaurus graph from the roget.dat example in
    the Stanford Graph Base.
    """
    try:
        fh=open("roget.dat","r")
    except IOError:
        print "roget.dat not found"
        raise

    G=DiGraph()

    for line in fh.readlines():
        if line.startswith("*"): # skip comments
            continue
        if line.startswith(" "): # this is a continuation line, append
            line=oldline+line
        if line.endswith("\\\n"): # continuation line, buffer, goto next
            oldline=line.strip("\\\n")
            continue

        (headname,tails)=line.split(":")

        # head
        numfind=re.compile("^\d+") # re to find the number of this word
        head=numfind.findall(headname)[0] # get the number
    
        G.add_node(head)

        for tail in tails.split():
            if head==tail:
                print >>sys.stderr,"skipping self loop",head,tail
            G.add_edge(head,tail)

    return G            

if __name__ == '__main__':
    from NX import *
    G=roget_graph()
    print "Loaded Donald Knuth's roget.dat containing 1022 categories."
    print "digraph has %d nodes with %d edges"\
          %(number_of_nodes(G),number_of_edges(G))
    print number_connected_components(G),"connected components"

