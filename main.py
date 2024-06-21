from classes.overlapping_neighbors_class import OverlappingNeighbors
from classes.overlapping_neighbors_v2_class import OverlappingNeighborsV2
from classes.overlapping_neighbors_v3_class import OverlappingNeighborsV3
from classes.protein_degree_class import ProteinDegree
from classes.protein_degree_v2_class import ProteinDegreeV2
from classes.protein_degree_v3_class import ProteinDegreeV3
from classes.sample_algorithm import SampleAlgorithm
from classes.hypergeometric_distribution_class import HypergeometricDistribution
from classes.hypergeometric_distribution_class_V2 import HypergeometricDistributionV2

import matplotlib.pyplot as plt
from random import sample
from pathlib import Path
import os
import sys
import pandas as pd
import statistics as stat
from colorama import init as colorama_init
from tools.helper import (
    create_ppi_network,
    read_specific_columns,
    export_graph_to_pickle,
    read_pro_go_data,
)
from tools.workflow import run_workflow


def main():
    colorama_init()
    if not os.path.exists("output"):
        os.makedirs("output")
    if not os.path.exists("output/dataset"):
        os.makedirs("output/dataset")
    if not os.path.exists("output/data"):
        os.makedirs("output/data")
    if not os.path.exists("output/images"):
        os.makedirs("output/images")

    fly_interactome_path = Path("./network/fly_propro.csv")
    fly_go_association_path = Path("./network/fly_proGo.csv")
    zfish_interactome_path = Path("./network/zfish_propro.csv")
    zfish_go_association_path = Path("./network/zfish_proGo.csv")
    bsub_interactome_path = Path("./network/bsub_propro.csv")
    bsub_go_association_path = Path("./network/bsub_proGo.csv")

    output_data_path = Path("./output/data/")
    output_image_path = Path("./output/images/")
    dataset_directory_path = Path("./output/dataset")
    graph_file_path = Path(dataset_directory_path, "graph.pickle")
    sample_size = 10
    repeats = 10
    new_random_lists = True

    testing_output_data_path = Path("./output/data/")
    testing_output_image_path = Path("./output/images/")
    testing_input_directory_path = Path("./tests/testing-dataset/")
    testing_graph_file_path = Path(testing_input_directory_path, "graph.pickle")

    namespace = ["molecular_function", "biological_process", "cellular_component"]
    # change the go_term_type variable to include which go term namespace you want
    go_term_type = [namespace[0], namespace[1], namespace[2]]
    short_name = ""
    if namespace[0] in go_term_type:
        short_name = short_name + "_mol"
    if namespace[1] in go_term_type:
        short_name = short_name + "_bio"
    if namespace[2] in go_term_type:
        short_name = short_name + "_cel"

    interactome_columns = [0, 1]
    interactome = read_specific_columns(fly_interactome_path, interactome_columns, ",")

    go_inferred_columns = [0, 2, 3]
    go_protein_pairs = read_pro_go_data(
        fly_go_association_path, go_inferred_columns, go_term_type, ","
    )

    protein_list = []

    # if there is no graph.pickle file in the output/dataset directory, uncomment the following lines
    G, protein_list = create_ppi_network(interactome, go_protein_pairs)
    export_graph_to_pickle(G, graph_file_path)

    # Define algorithm classes and their names
    algorithm_classes = {
        "OverlappingNeighbors": OverlappingNeighbors,
        "OverlappingNeighborsV2": OverlappingNeighborsV2,
        "OverlappingNeighborsV3": OverlappingNeighborsV3,
        "ProteinDegree": ProteinDegree,
        "ProteinDegreeV2": ProteinDegreeV2,
        "ProteinDegreeV3": ProteinDegreeV3,
        "SampleAlgorithm": SampleAlgorithm,
        "HypergeometricDistribution": HypergeometricDistribution,
        "HypergeometricDistributionV2": HypergeometricDistributionV2,
    }

    run_workflow(
        algorithm_classes,
        go_protein_pairs,
        sample_size,
        protein_list,
        graph_file_path,
        dataset_directory_path,
        output_data_path,
        output_image_path,
        repeats,
        new_random_lists,
        short_name,
    )

    sys.exit()


if __name__ == "__main__":
    main()
