#!/bin/bash -l

eval "$(conda shell.bash hook)"
echo "INFO: Activating conda environment"
conda activate plot_env
echo "INFO: Creating plot"
snakemake -s support_files/plot.snf --cores 1 -p 2> pipeline.log
echo "INFO: conda deactivate"
conda deactivate
echo "INFO: done!"
