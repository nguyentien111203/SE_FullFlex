import FlexSliceMappingProblem as FSMP
import networkx as nx
import matplotlib.pyplot as plt

phy_generator = FSMP.phy.fromgml_rw.FromGmlGraphGenerator(
    gml_path="./data/__internals__/SndLib/abilene.gml",
    nodecap=[100,100,100],
    linkcap=[100]
)

PHY = phy_generator.Generate()

nx.draw_networkx(PHY, pos = PHY.NodeLocations)

plt.show()