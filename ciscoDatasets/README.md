# Cisco Network Motif Mining Using SPMiner

This repository contains my work on preparing, processing, and mining motifs from a Cisco network communication dataset using SPMiner, a neural subgraph pattern mining framework.
The goal of this project is to automatically discover communication patterns (motifs) from real network traffic and interpret their meaning in a social/organizational context.

## Project Overview

Traditional networks are large and complex, making manual inspection of patterns impossible.
Motifs — recurring subgraph structures, help reveal meaningful behaviors such as:
- Social dynamics
- Collaboration styles
- Fraud or suspicious communication patterns
- Role-based interactions
- Structural anomalies

This project uses SPMiner (Neural Subgraph Matcher & Miner) to automatically discover such motifs from a real-world Cisco Secure Workload dataset.

## Dataset

The dataset used is:
```
CiscoSecureWorkload_22_networks
└── dir_g21_small_workload_with_gt
    └── dir_no_packets_etc
        └── dir_few_sensors
            ├── edges_1days_tillFeb9_partial_sensors.csv.txt
            └── README
```

Key properties:
- Only a subset of nodes (31 out of ~50) were observed due to limited sensors
- Directed edges with detailed protocol/port interaction counts
- Rich multi-attribute edge data suitable for motif mining

### 1. Dataset Preparation

The script convert_to_spminer.py parses the Cisco dataset and converts it to the SPMiner-required PKL format.

Input Format

Each line in the Cisco file looks like:
```
g21 0 1 1p17-1,3p17-1,1p6-1
```
Output Format

A PKL file containing:
```
[
   NetworkX DiGraph with:
      - nodes: integer host IDs
      - edges: directed edges with attributes:
          * counts
          * ports
          * protocols
]
```
Run the converter
```
python convert_to_spminer.py
```

Produces:
```
ciscoDatasets/spminer_input.pkl
Nodes: 31
Edges: 690
Directed: True
```
### 2. Running SPMiner on the Cisco Dataset

SPMiner is run using the pretrained decoder model.

Command
```
python -m subgraph_mining.decoder \
    --dataset=custom \
    --graph_pkl_path=ciscoDatasets/spminer_input.pkl \
    --graph_type=directed \
    --node_anchored
```
Output Summary
- Runtime: ~74 seconds
- Graphs processed: 1
- Patterns discovered: 272
- Unique motif instances: 74
- Unique motif types: 9
- Duplicate removal rate: 72.8%
- Visualizations saved to: plots/cluster/
- Pattern results saved to:
   - results/out-patterns_all_instances.pkl
   - results/out-patterns.json

### 3. Motif Analysis Summary

(Full analysis provided in the project report)

Key findings:

Most common motifs
- Dense triads (3-node motifs)
- 4-node clusters with bidirectional traffic
- 5-node communication hubs

These appear to correspond to:
- Service clusters
- Frequently interacting machine groups
- Gateway communication structures
- Possible load-balanced patterns

Strengths of SPMiner
- Automatically discovers dense communication structures
- Removes duplicate patterns efficiently
- Handles multi-attribute edge features
- High parallel performance via multiprocessing

Limitations Observed
- Ignores semantic metadata (device type, role, service)
- Visualization labels are limited (Cisco input lacks labels)
- Misses long-range temporal patterns
- Does not infer anomaly severity

Potential Improvements
- Integrate host-level metadata (device type, subnet, application role)
- Include text features (log messages / descriptions)
- Add temporal segmentation to detect evolution of motifs
- Use clustering to group similar motif structures
- Improve visualization with meaningful labels

Repository Structure
```
neural-subgraph-matcher-miner/
│
├── ciscoDatasets/
│   ├── edges_1days_tillFeb9_partial_sensors.csv.txt
│   ├── spminer_input.pkl
│   └── convert_to_spminer.py
│
├── subgraph_mining/
│   ├── decoder.py
│   ├── encoder.py
│   └── common/
│
├── results/
│   ├── out-patterns_all_instances.pkl
│   ├── out-patterns.json
│   └── ...
│
└── plots/
    └── cluster/
        └── interactive motif visualizations
```
How to Reproduce the Results
1. Clone the repository
2. Install dependencies (requirements.txt)
3. Convert the Cisco dataset:
```
python convert_to_spminer.py
```

4. Run SPMiner:
```
python -m subgraph_mining.decoder --dataset=custom --graph_pkl_path=ciscoDatasets/spminer_input.pkl --graph_type=directed --node_anchored

```
5. View results:
- PKLs inside results/
- Interactive graphs in plots/cluster/

## Credits
- Cisco for the original dataset
- SPMiner authors (RejuveBio)
- iCog Labs
