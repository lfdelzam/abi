## Objective ##

Course applied bioinfomatic - Medbioinfo

This pipleine creates a boxplot, comparing the number of domains of proteins with node degrees > and to the ones with node degrees <= user-defined cutoff, for a protein network where the edges weight are larger or equal to an user-defined threshold


## Installation ##

1) Download the pipeline:

			git clone https://github.com/lfdelzam/abi

2) Installation of required software/packages:

			bash install_packages.sh

## Usage ##

1) modified parameter in config file:

			nano support_files/plot_config.JSON


	"working_dir": "/absolute/path/to/abi/",
  "protein_network_data":"/absolute/path/to/protein/edges/file", -- 9606.protein.links.v11.0.txt --
  "protein_domain_file":"/absolute/path/to/protein/domains/file", -- proteins_w_domains.txt --
  "output_prefix_name_fig": "protein_domains_vs_string_degree",
  "node_degree_cutoff": 100,
  "weigth_thresold": 500

save changes by typing  `CTRL+X` and `Y`

2) run the pipeline:

			bash run_pipeline.sh

## Output ##

The png figures are will be placed in the directory `FIGURES_node_degree_<node_degree_cutoff>_W_<weigth_thresold>`
The pipelone log file is stored in the working directory with the name `pipeline.log`
