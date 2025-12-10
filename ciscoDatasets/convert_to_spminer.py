import pickle
import networkx as nx

EDGE_FILE = "ciscoDatasets/edges_1days_tillFeb9_partial_sensors.csv.txt"
OUTPUT_PKL = "ciscoDatasets/spminer_input.pkl"

def parse_edge_attributes(attr_string):
    parts = attr_string.split(",")
    counts, ports, protocols = [], [], []

    for p in parts:
        try:
            count_str, rest = p.split("p")
            port_str, proto_str = rest.split("-")
            counts.append(int(count_str))
            ports.append(int(port_str))
            protocols.append(int(proto_str))
        except:
            continue

    return {
        "counts": counts,
        "ports": ports,
        "protocols": protocols
    }

def load_cisco_graph(path):
    G = nx.DiGraph()

    with open(path, "r") as f:
        for line in f:
            parts = line.strip().split()

            if len(parts) < 4:
                continue

            src = int(parts[1])
            dst = int(parts[2])
            attr_str = parts[3]

            attr = parse_edge_attributes(attr_str)

            G.add_node(src)
            G.add_node(dst)
            G.add_edge(src, dst, **attr)

    return G

if __name__ == "__main__":
    G = load_cisco_graph(EDGE_FILE)

    graphs = [G]

    with open(OUTPUT_PKL, "wb") as f:
        pickle.dump(graphs, f)

    print("Saved SPMiner graph to:", OUTPUT_PKL)
    print("Nodes:", G.number_of_nodes())
    print("Edges:", G.number_of_edges())
    print("Directed:", G.is_directed())
