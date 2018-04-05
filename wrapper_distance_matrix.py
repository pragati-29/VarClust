#!/usr/bin/env python3

# Load modules
import read_profiles
import argparse
from distance_matrix import calculate_distance_matrix

# Argument parser -------------------------------------------------------------

parser = argparse.ArgumentParser(epilog='Calculates a distance matrix for the '
                                        'chosen metric of all SNV profiles in '
                                        'the input directory.')
parser.add_argument('input_dir',
                    type=str,
                    help='input directory path containing the SNV profiles')
parser.add_argument('output',
                    type=str,
                    help='output distance matrix file path')
parser.add_argument('-m', '--metric',
                    type=str,
                    dest='metric',
                    default='cosine',
                    metavar='',
                    help='[cosine, euclidean, similarity_score, '
                          'distance_aware, correlation (default)]')
parser.add_argument('-M', '--merge',
                    type=str,
                    dest='merge',
                    default='inner',
                    metavar='',
                    help='merge method [inner or outer (default)]')
parser.add_argument('-s', '--subset_cols',
                    type=str,
                    dest='subset_cols',
                    default=None,
                    metavar='',
                    help='list of column(s) to subset variants on')
parser.add_argument('-S', '--subset_values',
                    type=str,
                    dest='subset_values',
                    default=None,
                    metavar='',
                    help='list of value(s) to subset variants on')
parser.add_argument('-n', '--do-not-normalise',
                    action='store_true',
                    dest='normalise',
                    help='do not normalise final distance matrix')
args = parser.parse_args()

# Analysis --------------------------------------------------------------------

# Read profiles
profiles = read_profiles.read_profile_dir(args.input_dir,
                                          args.subset_cols.split(','),
                                          args.subset_values.split(','))

# Calculate distances
dist = calculate_distance_matrix(profiles=profiles,
                                 metric=args.metric,
                                 merge=args.merge)

# Save distances
dist.to_csv(args.output, sep='\t')
