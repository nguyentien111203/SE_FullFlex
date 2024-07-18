import FlexSliceMappingProblem as FSMP
import networkx as nx
import matplotlib.pyplot as plt

phy_generator = FSMP.phy.fromgml_rw.FromGmlGraphGenerator(
    gml_path="./data/__internals__/SndLib/polska.gml",
    nodecap=[20,20,20],
    linkcap=[20]
)

PHY = phy_generator.Generate()

nx.draw_networkx(PHY, pos = PHY.NodeLocations)

plt.show()