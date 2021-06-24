#!/bin/bash -l
wd=$(pwd)
for a in "$@"
do
case $a in
  -p=*|--path_to_edge_file=*)
  if [ ! -z "${a#*=}" ];  then
      Filep="${a#*=}"
  fi
  shift # past argument
  ;;

  -d=*|--path_to_domain_file=*)
  if [ ! -z "${a#*=}" ];  then
      Filed="${a#*=}"
  fi
  shift # past argument
  ;;

  *)
  echo -e "\nUsage: bash run_pipeline.sh [options]\n -d=<path to protein domain file> -p=<path to protein edges file>\n"
  echo -e "   if -d and -p not provided, paths will be obtained from support_files/plot_config.JSON\n"
  exit 0
  ;;

esac
done

eval "$(conda shell.bash hook)"
echo "INFO: Activating conda environment"
conda activate plot_env
echo "INFO: Creating plot"
if [ -s "$Filep" ] && [ -s "$Filed" ]; then
  snakemake -s support_files/plot.snf --config protein_network_data=$Filep protein_domain_file=$Filed working_dir=$wd --cores 1 -p
else
  snakemake -s support_files/plot.snf --cores 1 -p
fi
echo "INFO: conda deactivate"
conda deactivate
