#!/usr/bin/python

"""Checks the routing invariant for the routing table specified by the given
CSV files.

The first file must consist of one line for each node in the network, giving the
node names as a hexadecimal number. The first entry is the node whose routing
table is specified in the line. The remaining entries are the list of contacts
in its routing table.

The second file has the same syntax, but instead of the routing table entries
lists all the node's prefixes in binary.
"""

import sys
import csv

BITS = 24 # The length of the node names in bits.
MIN_GROUP_SIZE = 8 # Groups below this size are expected to be merged.
bin_str = "{:0" + str(BITS) + "b}" # Binary format string.

tables = {}
with open(sys.argv[1], 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if len(row) > 0 and not row[0].startswith("#"):
            tables[row[0].strip(". ").lower()] = set([i.strip(". ").lower() for i in row])

prefixes_by_node = {}
with open(sys.argv[2], 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if len(row) > 0 and not row[0].startswith("#"):
            prefixes_by_node[row[0].strip(". ")] = row[1:]
            if len(row) == 1:
                prefixes_by_node[row[0].strip(". ")] = [""]

def matches(node, pfx):
    """ Returns whether the node name matches the prefix. """
    return bin_str.format(int(node, 16)).startswith(pfx)

# Collect all prefixes, verify they are pairwise incompatible and sort the nodes
# by prefix. Check that each group has the minimum required size.
groups = {}
for name in prefixes_by_node:
    for pfx in prefixes_by_node[name]:
        if pfx not in groups:
            for group_pfx in groups:
                if group_pfx.startswith(pfx) or pfx.startswith(group_pfx):
                    print("Compatible prefixes: {}, {}".format(pfx, group_pfx))
            groups[pfx] = set([n for n in tables if matches(n, pfx)])
            if pfx != "" and len(groups[pfx]) < MIN_GROUP_SIZE:
                print("Group {} has not enough entries: {}.".format(pfx, groups[pfx]))

# Verify that the prefixes cover the whole address space.
covered = [x for x in groups.keys()]
while len(covered) > 1:
    covered.sort(key = len)
    merge_pfx = covered[-1][:-1]
    if merge_pfx + "0" not in covered or merge_pfx + "1" not in covered:
        print("Prefix {} not covered.".format(merge_pfx))
    covered = [pfx for pfx in covered if not pfx.startswith(merge_pfx)] + [merge_pfx]
if covered != [""]:
    print("Not all prefixes covered, only {}.".format(covered))

pfxs = {}
for pfx in groups:
    for name in groups[pfx]:
        pfxs[name] = pfx

# Verify that each node has the required contacts.
for name in tables:
    expected = set()
    for other in groups:
        if sum(1 for (x, y) in zip(other, pfxs[name]) if x != y) <= 1:
            expected |= groups[other]
    if expected != tables[name]:
        missing = expected - tables[name]
        unexpected = tables[name] - expected
        if len(missing) > 0:
            print("{} is missing {}.".format(name, missing))
        if len(unexpected) > 0:
            print("{} shouldn't have {}.".format(name, unexpected))
