import pickle
import os
from collections import defaultdict

# Configuration
EDGE_FILE = "Dataset\edges_1days_tillFeb9_partial_sensors.csv.txt"   
OUTPUT_PKL = "spminer_input.pkl"                             

# Parse a single attribute string into python dictionary features
def parse_edge_attributes(attr_string):
    """
    Convert strings like:
      "1p17-1,3p17-1,1p6-1"
    into:
      {'counts': [1,3,1], 'ports':[17,17,6], 'protocols':[1,1,1]}
    """
    parts = attr_string.split(",")
    counts, ports, protocols = [], [], []

    for p in parts:
        # Example:  "3p17-1"
        try:
            count_str, rest = p.split("p")
            port_str, proto_str = rest.split("-")

            counts.append(int(count_str))
            ports.append(int(port_str))
            protocols.append(int(proto_str))
        except:
            # Ignore malformed entries
            continue

    return {
        "counts": counts,
        "ports": ports,
        "protocols": protocols
    }


# Load the Cisco edge file
def load_cisco_graph(path):
    print(f"Loading graph from: {path}")

    edges = []
    nodes = set()

    with open(path, "r") as f:
        for line in f:
            parts = line.strip().split()

            if len(parts) < 4:
                continue

            graph_id = parts[0]      # "g21"
            src = int(parts[1])
            dst = int(parts[2])
            attr_string = parts[3]

            attr = parse_edge_attributes(attr_string)

            # store directed edge
            edges.append((src, dst, attr))

            # collect nodes
            nodes.add(src)
            nodes.add(dst)

    print(f"Loaded: {len(nodes)} nodes, {len(edges)} edges")
    return list(nodes), edges


# Save into SPMiner format
def save_spminer_format(nodes, edges, output_path):
    """
    SPMiner expects a pickle containing a Python dictionary.
    We will use:

    {
       "nodes": [list of node ids],
       "edges": [
            (src, dst, feature_dict)
       ]
    }
    """
    graph_dict = {
        "nodes": nodes,
        "edges": edges
    }

    with open(output_path, "wb") as f:
        pickle.dump(graph_dict, f)

    print(f"✔ Saved SPMiner dataset to: {output_path}")


# Main pipeline
if __name__ == "__main__":
    nodes, edges = load_cisco_graph(EDGE_FILE)
    save_spminer_format(nodes, edges, OUTPUT_PKL)