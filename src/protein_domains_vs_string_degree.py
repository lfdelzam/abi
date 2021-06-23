# /usr/bin/env python3
import os
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

usage = 'python protein_domains_vs_string_degree.py [-i] [-d] [-o] [-c] [-s] '
description = 'This program creates a boxplot, comparing the number of domains of proteins with \
                node degrees > and to the ones with node degrees <= user-defined cutoff, \
                for a protein network where the edges weight are larger or equal to an user-defined threshold'

parser = argparse.ArgumentParser(description=description, usage=usage)
parser.add_argument(
    '-i',
    metavar="input file protein links",
    dest='i',
    help='9606.protein.links.v11.0.txt',
    required=True)
parser.add_argument(
    '-d',
    metavar="input file protein domains",
    dest='d',
    help='proteins_w_domains.txt',
    required=True)
parser.add_argument(
    '-o',
    metavar="output prefix file name",
    dest='o',
    help='protein_domains_vs_string_degree',
    required=True)
parser.add_argument(
    '-c',
    metavar="node degree cutoff",
    dest='c',
    help='node degree cutoff, default 100',
    default=100)
parser.add_argument(
    '-s',
    metavar="combined score threshold",
    dest='s',
    help='combined score threshold, default 500',
    default=500)

args = parser.parse_args()


def Proteins_with_domain_n_degree_cutoff(type):
    # selecting nodes
    if type == "h":
        proteins_n_degree = {
            n.split(".")[1]: d for n,
            d in network.degree if d > int(args.c) }
    else:
        proteins_n_degree = {
            n.split(".")[1]: d for n,
            d in network.degree if d <= int(args.c) }

    # converting dict into DataFrame
    df_proteins_n_degree = pd.DataFrame(
        proteins_n_degree.items(), columns=[
            'Protein stable ID', 'node degree'])
    Proteins_with_domain_n_degree = pd.merge(
        domain_df, df_proteins_n_degree, on='Protein stable ID')

    return Proteins_with_domain_n_degree


def counting_domains(protein_df, type):
    # counting domains
    serie = protein_df['Protein stable ID'].value_counts(ascending=True)
    # convering into DataFrame
    p_df = serie.to_frame()
    p_df.reset_index(level=0, inplace=True)
    p_df.columns = ['Protein stable ID', 'Number domains']
    # adding label
    if type == "h":
        p_df["node degree"] = "> " + str(args.c)
    else:
        p_df["node degree"] = "<= " + str(args.c)

    return p_df


def plotting(df1, df2, kind):

    # concatenating results
    protein_domains_vs_string_degree_df = pd.concat([df1, df2])
    #plotting and saving
    plt.figure(figsize=(10, 8))
    if kind == "boxplot":
        g = sns.boxplot(
            x="Number domains",
            y="node degree",
            data=protein_domains_vs_string_degree_df,
            linewidth=0.5,
            showmeans=True,
            meanprops={
                "marker": "o",
                "markerfacecolor": "white",
                "markeredgecolor": "black",
                "markersize": "5"})

        plt.savefig(args.o+".png", format='png', dpi=150)

        g.set_xscale("log")
        plt.savefig(args.o+"_log.png", format='png', dpi=150)

    else:
        g = sns.violinplot(
            x="Number domains",
            y="node degree",
            data=protein_domains_vs_string_degree_df)
        plt.savefig(args.o+"_violinplot.png", format='png', dpi=150)



# reading input files
# domain files
domain_df = pd.read_csv(args.d, sep='\t')
# name of the column contianing the protein IDs
column_protein_IDs_index = [i for i in range(
    0, len(domain_df.columns)) if domain_df.iloc[0, i].startswith("ENSP")][0]
# making sure the name is standard and can be used for other input files
domain_df.columns.values[int(column_protein_IDs_index)] = 'Protein stable ID'
domain_df.dropna(inplace = True)

# Protein edges files
df = pd.read_csv(args.i, sep=' ')
# making sure weight column is numeric
df.dropna(inplace = True)
df.iloc[:, 2] = pd.to_numeric(df.iloc[:, 2])

# selecting data before creating the network
network_data_frame = df[df.iloc[:, 2] >= int(args.s)]

# building network
network = nx.from_pandas_edgelist(
    network_data_frame,
    network_data_frame.columns[0],
    network_data_frame.columns[1],
    edge_attr=network_data_frame.columns[2])

# selecting proteins according to node degree cutoff
Proteins_with_domain_n_degree_h = Proteins_with_domain_n_degree_cutoff("h")
Proteins_with_domain_n_degree_be = Proteins_with_domain_n_degree_cutoff("be")
# counting domains per selected proteins
Prot_h = counting_domains(Proteins_with_domain_n_degree_h, "h")
Prot_be = counting_domains(Proteins_with_domain_n_degree_be, "be")
plotting(Prot_be, Prot_h, "boxplot")
plotting(Prot_be, Prot_h, "violinplot")
