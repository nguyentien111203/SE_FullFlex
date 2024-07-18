import uuid

from .__internals__ import *

class LinearSliceGenerator(SliceGenerator):
    def __init__(self, mode:str):
        self.mode = mode
        pass

    def Generate(self) -> nx.DiGraph:
        match self.mode:
            case "mix":
                SFC = Generate_SfcConfigMix()
            case "config1":
                SFC = Generate_SfcConfigStatic1()
            case "config2":
                SFC = Generate_SfcConfigStatic2()
            case _:
                raise Exception("Not implemented.")
        return SFC

NODES = [
    (0, {
        "name":"SensorDataAcquision",
        "label":"SDA",
        "req":NodeResource(10, 0, 15)
    }),
    (1, {
        "name":"DataPreprocessing",
        "label":"DP",
        "req":NodeResource(15, 0, 15)
    }),
    (2, {
        "name":"DataCompression",
        "label":"DC",
        "req":NodeResource(20,0,15)
    }),
    (3, {
        "name":"Security",
        "label":"SEC",
        "req":NodeResource(10,0,10)
    }),
    (4, {
        "name":"IndustrialAnalytics",
        "label":"IA",
        "req":NodeResource(10,0,10)
    }),
    (5, {
        "name":"Command&Control",
        "label":"CC",
        "req":NodeResource(10,0,10)
    })
]

LINKS = {
    (0,1): LinkResource(20),
    (1,2): LinkResource(20),
    (1,3): LinkResource(20),
    (2,3): LinkResource(20),
    (3,2): LinkResource(1),
    (3,4): LinkResource(1),
    (2,4): LinkResource(1),
    (4,5): LinkResource(1),
}
    
def Generate_SfcConfigMix() -> nx.DiGraph:
    SFC = nx.DiGraph()
    
    SFC.add_nodes_from(NODES)
    
    SFC.FixedPositions = []
    SFC.FixedPositions.append((0,0))
    SFC.FixedPositions.append((1,1))
    SFC.FixedPositions.append((4,4))
    SFC.FixedPositions.append((5,5))
    
    SFC.LinkRequirement = LINKS
    
    SFC.name = f"linear_realworld_configmix_{uuid.uuid4().hex[:8]}"
    
    return SFC

def Generate_SfcConfigStatic1() -> nx.DiGraph:
    SFC = nx.DiGraph()
    
    SFC.add_nodes_from(NODES)
    
    SFC.FixedPositions = []
    SFC.FixedPositions.append((0,0))
    SFC.FixedPositions.append((1,1))
    SFC.FixedPositions.append((2,2))
    SFC.FixedPositions.append((3,3))
    SFC.FixedPositions.append((4,4))
    SFC.FixedPositions.append((5,5))
    
    SFC.LinkRequirement = LINKS
    
    SFC.name = f"linear_realworld_config1_{uuid.uuid4().hex[:8]}"
    
    return SFC

def Generate_SfcConfigStatic2() -> nx.DiGraph:
    SFC = nx.DiGraph()
    
    SFC.add_nodes_from(NODES)
    
    SFC.FixedPositions = []
    SFC.FixedPositions.append((0,0))
    SFC.FixedPositions.append((1,1))
    SFC.FixedPositions.append((2,3))
    SFC.FixedPositions.append((3,2))
    SFC.FixedPositions.append((4,4))
    SFC.FixedPositions.append((5,5))
    
    SFC.LinkRequirement = LINKS
    
    SFC.name = f"linear_realworld_config2_{uuid.uuid4().hex[:8]}"
    
    return SFC