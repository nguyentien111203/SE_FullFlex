import networkx as nx
import random
import FlexSliceMappingProblem as FSMP
import matplotlib.pyplot as plt



"""
    Arguments : 
        numconf : number of configuration (2 < conf < 4)
    Output : 
        GS : A graph represent a configuration of a slice
    
    This function is used to create a configuration graph for a slice
"""
def generate_config_slice(numconf : int,
                          config_list : list):

    # Take the number of config
    count = numconf

    # Create a list of configuration
    GS = list()

    # Create 4 configuration of a slice
    if ('C1' in config_list):
        k1 = nx.DiGraph()
        k1.add_node(0,cap=FSMP.sfc.NodeResource(20,20,20))
        k1.add_node(1,cap=FSMP.sfc.NodeResource(15,15,15))
        k1.add_node(2,cap=FSMP.sfc.NodeResource(20,20,20))
        k1.add_node(3,cap=FSMP.sfc.NodeResource(15,15,15))

        k1.add_edge(0,1,cap=FSMP.sfc.LinkResource(15))
        k1.add_edge(1,2,cap=FSMP.sfc.LinkResource(15))
        k1.add_edge(2,3,cap=FSMP.sfc.LinkResource(15))
    
        GS.append(k1)
        count-=1

    if ('C2' in config_list):
        k2 = nx.DiGraph()
        k2.add_node(0,cap=FSMP.sfc.NodeResource(20,20,20))
        k2.add_node(1,cap=FSMP.sfc.NodeResource(10,10,10))
        k2.add_node(2,cap=FSMP.sfc.NodeResource(5,5,5))
        k2.add_node(3,cap=FSMP.sfc.NodeResource(5,5,5))

        k2.add_edge(0,1,cap=FSMP.sfc.LinkResource(10))
        k2.add_edge(1,2,cap=FSMP.sfc.LinkResource(5))
        k2.add_edge(1,3,cap=FSMP.sfc.LinkResource(5))

        GS.append(k2)
        count-=1
    
    if ('C3' in config_list) :
        k3 = nx.DiGraph()
        k3.add_node(0,cap=FSMP.sfc.NodeResource(20,20,20))
        k3.add_node(1,cap=FSMP.sfc.NodeResource(10,10,10))
        k3.add_node(2,cap=FSMP.sfc.NodeResource(20,20,20))
        k3.add_node(3,cap=FSMP.sfc.NodeResource(10,10,10))

        k3.add_edge(0,1,cap=FSMP.sfc.LinkResource(10))
        k3.add_edge(1,2,cap=FSMP.sfc.LinkResource(20))
        k3.add_edge(3,2,cap=FSMP.sfc.LinkResource(20))
        k3.add_edge(0,3,cap=FSMP.sfc.LinkResource(10))
        
        GS.append(k3)
        count-=1

    return GS


"""
    Arguments : 
        numnodes : number of nodes
    Output : 
        PHY : A graph represent physical network
    
    This function is used to create physical network graph
"""
def CreatePHYGraph():
    # Create a generator
    phy_generator = FSMP.phy.fromgml_rw.FromGmlGraphGenerator(
        gml_path="./data/__internals__/SndLib/abilene.gml",
        nodecap=[40,40,40],
        linkcap=[40]
    )

    PHY = phy_generator.Generate()

    return PHY


"""
    Arguments : 
        numslices : number of slices
        numconf : number of config for each slice
    Output : 
        K : A list of list of configuration of slices
    
    This function is used to create a set of configuration of each slices
"""
def CreateSlicesSet(numslices : int,
                    numconf : int,
                    config_list : list):
    # Create a list of slices
    K = list()
    for i in range(numslices):
        # Create a list of configuration for each slice
        K.append(generate_config_slice(numconf, config_list))

    return K