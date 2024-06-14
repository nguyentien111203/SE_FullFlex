from .__internals__ import *
from .sfc import GetAllPossibleVirtualEdge, GetVLinkReq_safe
from .resources import NodeResource, LinkResource, ZERO_LINK_RESOURCE, ZERO_NODE_RESOURCE

import pulp
import networkx as nx
import copy

class SolutionData:
    def __init__(self, data):
        self.data_dict = data

    def __call__(self, key=None):
        return round(self.data_dict.get(key, 0),0)

    def __len__(self):
        return len(self.data_dict)
    
def ValidateSolution(prob: SliceMappingProblem, debug:bool=False, ndigits:int=5) -> SliceMappingProblem:
    PHY = prob.PHY
    SFC_SET = prob.SFC_SET
    solution = prob.solution
    result = validatesolution(PHY, SFC_SET, solution, ndigits)
    prob.solution_status = result
    return prob

def validatesolution(PHY, SFC_SET, solution, ndigits) -> SliceMappingProblem:
    if (not len(solution)):
        return 0
    solutiondata = SolutionData(solution)
    SFC_SET = assemble_sfc_from_solution(solutiondata, SFC_SET)
    # for sfc in SFC_SET:
    #     print(sfc.nodes)
    #     print(sfc.edges)
    if not SFC_SET:
        return -100
    xNode, xEdge, xSFC, y, z = VarsInit(PHY, SFC_SET)
    ## C1: Node Capacity
    for attr_i in range(len(ZERO_NODE_RESOURCE)):
        for node in PHY.nodes:
            if not (
                round(sum(
                    sum(
                        solutiondata(xNode[SFC_SET.index(sfc)][node_S][node].name) * nx.get_node_attributes(sfc, "req")[node_S][attr_i]
                            for node_S in sfc.nodes
                    ) 
                    for sfc in SFC_SET
                ), ndigits=ndigits)
                    <= nx.get_node_attributes(PHY, "cap")[node][attr_i]
            ):
                a= round(sum(
                    sum(
                        solutiondata(xNode[SFC_SET.index(sfc)][node_S][node].name) * nx.get_node_attributes(sfc, "req")[node_S][attr_i]
                            for node_S in sfc.nodes
                    ) 
                    for sfc in SFC_SET
                ), ndigits=ndigits)
                print(f"ERR:{a} {attr_i}, {nx.get_node_attributes(PHY, 'cap')[node][attr_i]}")
                return -1
    ## C2: Edge Capacity
    for attr_i in range(len(ZERO_LINK_RESOURCE)):
        for edge in PHY.edges:
            if not (
                round(sum(
                    sum(
                        solutiondata(xEdge[SFC_SET.index(sfc)][link_S][edge].name) * nx.get_edge_attributes(sfc, "req")[link_S][attr_i]
                        for link_S in sfc.edges
                    ) 
                    for sfc in SFC_SET
                ), ndigits=ndigits)
                    <= nx.get_edge_attributes(PHY, "cap")[edge][attr_i]
            ):
                return -2
    ## C3: Map 1 VNF - 1 PHYNODE
    for sfc in SFC_SET:
        for node in PHY.nodes:
            if not (
                sum(
                    solutiondata(xNode[SFC_SET.index(sfc)][node_S][node].name)
                    for node_S in sfc.nodes
                )
                <= solutiondata(xSFC[SFC_SET.index(sfc)].name)
            ):
                a= sum(
                    solutiondata(xNode[SFC_SET.index(sfc)][node_S][node].name)
                    for node_S in sfc.nodes
                )
                print(a,xSFC[SFC_SET.index(sfc)].name)
                print(solutiondata(xSFC[SFC_SET.index(sfc)].name))
                return -3
    ## C4.1: Map All VNF
    for sfc in SFC_SET:
        for node_S in sfc.nodes:
            if not (
                sum(
                    solutiondata(xNode[SFC_SET.index(sfc)][node_S][node].name)
                    for node in PHY.nodes
                )
                == solutiondata(xSFC[SFC_SET.index(sfc)].name)
            ):
                print(xSFC[SFC_SET.index(sfc)].name)
                return -4
    ## C5: Flow-Conservation
    for sfc in SFC_SET:
        for edge_S in sfc.edges:
            for node in PHY.nodes:
                if not (
                    sum(
                        solutiondata(str(xEdge[SFC_SET.index(sfc)][edge_S].get((node, nodej))))
                        for nodej in PHY.nodes
                    ) 
                    - 
                    sum(
                        solutiondata(str(xEdge[SFC_SET.index(sfc)][edge_S].get((nodej, node))))
                        for nodej in PHY.nodes
                    )
                    == solutiondata(xNode[SFC_SET.index(sfc)][edge_S[0]][node].name) - solutiondata(xNode[SFC_SET.index(sfc)][edge_S[1]][node].name)
                ):
                    return -5
                
    # C12 -- bs fixing
    if (str(PHY.name).__contains__("fattree")):
        for sfc in SFC_SET:
            if (not str(sfc.name).__contains__("bs")):
                continue
            k = SFC_SET.index(sfc)
            bs_nodes = [n for n in list(PHY.nodes) if nx.get_node_attributes(PHY, "kind")[n] == "host"]
            bs_vnodes = [n for n in list(sfc.nodes) if nx.get_node_attributes(sfc, "label")[n] == "BS"]
            if not (
                sum(
                    solutiondata(str(xNode[k][v][i]))
                    for v in sfc.nodes if v in bs_vnodes
                    for i in PHY.nodes if not i in bs_nodes
                ) == 0,
                f"C12_{k}"
            ):
                return -12
    return 1

def assemble_sfc_from_solution(solutiondata:SolutionData, SFC_SET):
    if (not len(solutiondata)):
        return 0
    traditional_SFC_SET = []
    for sfc in SFC_SET:
        traditional_sfc = copy.deepcopy(sfc)
        positions = []
        for v in sfc.nodes:
            for i in range(len(list(sfc.nodes))):
                if (solutiondata(f"t_{SFC_SET.index(sfc)}_{v}_{i}")):
                    positions.append((v,i))
        positions.sort(key=lambda pp:pp[1])
        if not (all(pp in positions for pp in sfc.FixedPositions)):
            if (solutiondata(f"xSFC_{SFC_SET.index(sfc)}")):
                return None
        positions = [p[0] for p in positions]
        for i in range(len(positions)-1):
            u, v = positions[i], positions[i+1]
            req = GetVLinkReq_safe(sfc, (u,v))
            traditional_sfc.add_edge(u,v,req=req)
        traditional_SFC_SET.append(traditional_sfc)
    
    return traditional_SFC_SET

def VarsInit(PHY, SFC_SET):
    # Variable stores building

    xNode = list()
    for sfc in SFC_SET:
        xNode.append(
            pulp.LpVariable.dicts(
                name=f"xNode_{SFC_SET.index(sfc)}",
                indices=(sfc.nodes, PHY.nodes),
                cat=pulp.LpBinary
            )
        )

    xEdge = list()
    for sfc in SFC_SET:
        all_possible_virtual_edges = GetAllPossibleVirtualEdge(sfc)
        xEdge.append(
            pulp.LpVariable.dicts(
                name=f"xEdge_{SFC_SET.index(sfc)}",
                indices=(all_possible_virtual_edges, PHY.edges),
                cat=pulp.LpBinary
            )
        )

    xSFC = pulp.LpVariable.dicts(
        name=f"xSFC",
        indices=(range(len(SFC_SET))),
        cat=pulp.LpBinary
    )

    y = list()
    for sfc in SFC_SET:
        all_possible_virtual_edges = GetAllPossibleVirtualEdge(sfc)
        y.append(
            pulp.LpVariable.dicts(
                name=f"y_{SFC_SET.index(sfc)}",
                indices=all_possible_virtual_edges,
                cat=pulp.LpBinary
            )
        )

    z = list()
    for sfc in SFC_SET:
        all_possible_virtual_edges = GetAllPossibleVirtualEdge(sfc)
        z.append(
            pulp.LpVariable.dicts(
                name=f"z_{SFC_SET.index(sfc)}",
                indices=(all_possible_virtual_edges, PHY.edges),
                cat=pulp.LpBinary
            )
        )
    
    return xNode, xEdge, xSFC, y, z
