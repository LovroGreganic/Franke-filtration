################################################################
# CALCULATION OF THE FRANKE FILTRATION FOR THE GLn
################################################################


################################################################
# IMPORTS
################################################################

import itertools
from itertools import product
import fractions as Fr
import networkx as nx

################################################################
# DETERMINING PARTITIONS INTO SEGMENTS
################################################################


def count_leading_without_jumps(exponents):
    """
    input:
        exponents (decreasing list of rational numbers)
    output:
        a number of how many leading, consecutive exponents differ by 0 or 1
    """
    i = 1
    while (len(exponents) != i and Fr.Fraction(exponents[i - 1]) - Fr.Fraction(exponents[i]) < 2):
        i += 1
    return i


def count_leading_repeats(exponents):
    """
        input:
            exponents (decreasing list of rational numbers)
        output:
            a number of how many leading, consecutive exponents coincide
    """
    i = exponents.count(exponents[0])
    return i




#exponents = decreasing list of rational numbers with last element being order of GLm
#segment = decreasing list of rational numbers differing by 1, with last two elements being number of representation and order of GLm;
#           eg. [b,b-1,...,a+1,a, rep_num, order]
#partition( of sequence) = list of segments partitioning sequence

def generate_combinations(list_of_partitions):
    return [sum(combination, []) for combination in product(*list_of_partitions)]


def mean(segment):
    """
        Returns the mean of the first len(segment)-3 elements.
        Used as a key in sorting segments.
        """

    return (Fr.Fraction((segment[0])) + Fr.Fraction(segment[len(segment) - 3])) / 2

def make_segment(size_of_segment, exponents, rep_num, order):
    """
    input:
        size_of_segment (int)
        exponents (decreasing list of rational numbers)
        rep_num (int, number of representation)
        order (int, size of GLm)
    output:
        segment of length size_of_segment out of elements of exponents
    """


    sof = size_of_segment
    segment = []
    i = 0

    segment.append(exponents[i])
    previous_element = exponents[i]  # remember previous element
    exponents.pop(i)  # and remove it
    while (sof != 0):
        if (previous_element == exponents[i]):  # disregard repeating elements
            i += 1
        else:
            segment.append(exponents[i])
            previous_element = exponents[i]
            exponents.pop(i)
            sof -= 1
    segment.append(rep_num)
    segment.append(order)
    return segment


def partition_into_segments(partitions_of_exponents, partition, sequence, l, rep_num,order):
    """
    A recursive function that partitions a list of exponents from the same representation and with the same denominator into segments.
    Parameters:
        partitions_of_exponents
        partition (partition to be added to the partitions_of_exponents)
        sequence (decreasing list of rational numbers)
        l (integer, starting length of segment to be added to partition)
        [next two parameters are important for making segments]
        rep_num (int, number of representation)
        order (int, size of GLm)
    """



    # BASE CASE: list 'exponents' is empty -> append 'segment'
    if (len(sequence) == 0):
        partitions_of_exponents.append(partition)
        return

    repeats = count_leading_repeats(sequence)
    w_j = count_leading_without_jumps(sequence)


    size = (Fr.Fraction(sequence[0]) - Fr.Fraction(sequence[w_j - 1]))
    size = Fr.Fraction(size).numerator  # size=int(size)

    if (repeats == w_j):
        """
                If, until first jump (consecutive exponents which are away by more than 1), all exponents are the same, 
                for each such exponent make an appropriate segment.
                eg:
                    [1,1,1,-1] => add [1],[1],[1] to partition. 
        """

        new_partition = partition.copy()
        new_exponents = sequence.copy()
        t = new_exponents[0]
        while (len(new_exponents) != 0 and t == new_exponents[0]):
            t = new_exponents[0]
            new_partition.append(make_segment(0, new_exponents,rep_num,order))

        partition_into_segments(partitions_of_exponents, new_partition, new_exponents, 0,rep_num,order)
        return

    new_partition = partition.copy()
    new_sequence = sequence.copy()
    new_partition.append(make_segment(size - l, new_sequence, rep_num, order))
    if (size - l != 0):
        partition_into_segments(partitions_of_exponents, partition, sequence, l + 1, rep_num, order)

    if (len(new_sequence) != 0 and new_sequence[0] == sequence[0]):
        partition_into_segments(partitions_of_exponents, new_partition, new_sequence, l, rep_num, order)
    else:
        partition_into_segments(partitions_of_exponents, new_partition, new_sequence, 0, rep_num, order)




def exponents_into_partitions(lists_of_exponents):
    """
    input:
        lists_of_exponents = lists of rational numbers in decreasing order, each belonging to different representation
    output:
        final_partitions = list of segments partitioning exponents
    """

    unordered_final_partitions = []
    # loop over each list of exponents separately
    # elements belonging to different exponents from lists_of_exponents can not belong to the same segment
    for rep_num in range(0,len(lists_of_exponents)):
        denomintaors = []
        # check for different denominators in list of exponents
        for i in range(0,len(lists_of_exponents[rep_num])-1):
            d = (lists_of_exponents[rep_num][i]).denominator
            if (d not in denomintaors):
                denomintaors.append(d)

        # elements with differenet denominators can not belong to the same segment
        for d in denomintaors:
            exponents_d = [] # exponents from lists_of_exponents[rep_num] with same denominators
            partitions = []
            for i in range(0,len(lists_of_exponents[rep_num])-1): # last element (order of GLm) is excluded
                denom = (lists_of_exponents[rep_num][i]).denominator
                if (denom == d):
                    exponents_d.append(lists_of_exponents[rep_num][i])

            order = lists_of_exponents[rep_num][len(lists_of_exponents[rep_num])-1] # last element
            partition_into_segments(partitions, [], exponents_d,0,rep_num+1,order)
            unordered_final_partitions.append(partitions)


    # combining partitions from last step into partition of Union(lists_of_exponents) (excluding last elements)
    combinations = generate_combinations(unordered_final_partitions)
    final_partitions=[]
    for i in combinations:

        i.sort(reverse=True, key=mean)  #sorting by mean of first length-3 elements

        final_partitions.append(i)
    return final_partitions

#############################################################
# DETERMINING LISTS OF z´s AND i(z)´s
##############################################################

# Z_np = list of z's
# z ( of partition) = tuple of elements (mean, rep_num, size) each corresponding to segment
#   where:
#       mean = mean of segment excluding last two elements
#       rep_num = number of representation of segment
#       size = order of GLm of segment times size of segment (b-a)
# Z = list of z's without rep_num and size
# iota_Z = list of iz's
# iz = (mean, mean, ..., mean ), with length of tuple = size

def permute_partial(list, start, end):
    """
    Returns a sequence of sequences, where each sequence has elements at indices [start, end] permutated.
    """

    # Extract the elements at the specified indices
    elements_to_permute = [list[i] for i in range(start, end + 1)]

    # Generate permutations of the selected elements
    permuted_elements = set(itertools.permutations(elements_to_permute))

    # List to hold the permuted versions of the original list
    result = []
    indices = []

    for i in range(start, end + 1):
        indices.append(i)

    # For each permutation, replace the permuted elements back into the original list
    for perm in permuted_elements:
        permuted_list = list[:]
        for idx, new_val in zip(indices, perm):
            permuted_list[idx] = new_val
        result.append(permuted_list)

    return result


def permute_z(list_of_perm, z, ind):
    """
    Recursive function that saves isomorphic copies of z into list_of_perm.
    We get isomorphic copies of z by permuting its elements with same value of first coordinate (mean)
    """

    if ind >= len(z):
        list_of_perm.append(z)
        return

    z_copy = z.copy()

    i = 0
    while (ind + i < len(z) and z[ind][0] == z[ind + i][0]):
        i = i + 1

    if i >= 2:

        perms = permute_partial(z_copy, ind, ind + i - 1)

        #perms in this case is a list of all segments with permuted elements with indices from start to ind+i-1

        for perm in perms:
            permute_z(list_of_perm, perm, ind + i)
    else:
        permute_z(list_of_perm, z_copy, ind + i)




def append_permutations(Z, iota_Z, z, z_mean,iz):
    """
    Appending elements to Z and iota_Z counting isomorphisms
    """
    list_of_perm = []
    permute_z(list_of_perm, z, 0)

    for _ in list_of_perm:
        Z.append(z_mean)
        iota_Z.append(iz)


def detailed_Z(partitions):
    """
        input:
            partitions (list of partitions of exponents into segments)
        output:
            Z_np (list of z's not counting isomorphisms)
            Z (list of z's without rep_num and size)
            iota_Z (list of iz's)
    """
    Z_np = []
    Z =[]
    iota_Z = []
    for partition in partitions:
        z = []
        z_mean = []
        iz = []
        for segment in partition:

            mean = (Fr.Fraction(segment[0]) + Fr.Fraction(segment[len(segment) - 3])) / 2
            rep_num = segment[len(segment) - 2]
            order = segment[len(segment) - 1]
            size = (len(segment) - 2)*order
            element = (mean, rep_num, size)


            z.append(element)
            z_mean.append(mean)
            for i in range(size):
                iz.append(mean)

        Z_np.append(tuple(z))

        append_permutations(Z, iota_Z,z, z_mean, iz)

    return Z_np, Z, iota_Z


def Z_without_morphisms(partitions):
    """
    input:
        partitions (list of partitions of exponents into segments)
    output:
        Z_np (list of z's not counting isomorphisms)
    """
    Z_np = []
    for partition in partitions:
        z = []
        for segment in partition:
            mean = (Fr.Fraction(segment[0]) + Fr.Fraction(segment[len(segment) - 3])) / 2
            rep_num = segment[len(segment) - 2]
            order = segment[len(segment) - 1]
            size = (len(segment) - 2) * order
            element = (mean, rep_num, size)
            z.append(element)
        Z_np.append(tuple(z))
    return Z_np


####################################################################
# DETERMINING PARTIAL ORDER AND FILTRATION
####################################################################




def iota(z):
    """
    Turning z into iz
    """
    iz = []
    for element in z:
        for i in range(element[2]):
            iz.append(element[0])

    return iz


def less(z1, z2):
    """
    Comparing iota(z1) and iota(z2)
    """
    iz1 = iota(z1)
    iz2 = iota(z2)
    if (iz1 == iz2):
        return False
    cumulative_sum_iz1 = Fr.Fraction(0)
    cumulative_sum_iz2 = Fr.Fraction(0)

    for a, b in zip(iz1, iz2):
        cumulative_sum_iz1 += Fr.Fraction(a)

        cumulative_sum_iz2 += Fr.Fraction(b)
        if cumulative_sum_iz1 < cumulative_sum_iz2:
            return False

    return True


def quotients(A, Z, less):


    G = nx.DiGraph()
    G.add_nodes_from(Z)

    for x in Z:
        for y in Z:
            if less(x, y):
                G.add_edge(x, y)

    G = nx.transitive_reduction(G)

    while G.nodes:
        maxs = [n for n in G.nodes if G.out_degree(n) == 0]
        A.append(list(maxs))
        G.remove_nodes_from(maxs)
    return A



def detailed_filtration(lists_of_exponents):
    """
        input:
            lists_of_exponents = lists of rational numbers in decreasing order with last element being order of GLm,
                                 each belonging to different representation
        output:
            A (list of quotients in Franke filtration, 0-th index corresponding to A^0/A^1; quotients are represented by z's)
            Z (list of z's without rep_num and size)
            iota_Z (list of iz's)
            list_of_partitions (partitions of exponents into segments)
        """

    list_of_partitions=exponents_into_partitions(lists_of_exponents)
    Z_np, Z, iota_Z = detailed_Z(list_of_partitions)
    A = []

    Z_copy = Z_np.copy()
    A = quotients(A, Z_copy, less)

    A.reverse()
    return A, Z, iota_Z, list_of_partitions



def filtration(lists_of_exponents):
    """
    input:
        lists_of_exponents = lists of rational numbers in decreasing order with last element being order of GLm,
                             each belonging to different representation
    output:
        A (list of quotients in Franke filtration, 0-th index corresponding to A^0/A^1; quotients are represented by z's)
    """

    list_of_partitions=exponents_into_partitions(lists_of_exponents)
    Z=Z_without_morphisms(list_of_partitions)
    A = []

    Z_copy = Z.copy()

    A = quotients(A, Z_copy, less)

    A.reverse()
    return A



################################################
# FUNCTIONS FOR PRINTING FILTRATION
################################################



def check_auto(summand):
    start = 0
    auto = []
    for i in range(1, len(summand)):

        if (summand[i] != summand[i - 1]):

            if (i - start > 1):
                auto.append(i - start)
            start = i
        if (summand[i] == summand[i - 1] and i == len(summand) - 1):
            auto.append(i - start + 1)
    return auto


def print_summand(summand, t):
    auto = check_auto(summand)

    if (len(auto) != 0):

        if (t):
            print("colim", auto, "{[", summand, "]}", " + ", end="")
        else:
            print("colim", auto, "{[", summand, "]}")

    else:
        if (t):
            print("{[", summand, "]}", " + ", end="")
        else:
            print("{[", summand, "]}")


def print_filtration(A):
    for i in range(len(A)-1):
        print("A^", i, "/A^", i + 1, " = ", end="")
        for j in range(len(A[i])):
            if (j != len(A[i]) - 1):

                print_summand(A[i][j], 1)
            else:
                print_summand(A[i][j], 0)

    print("A^", len(A) - 1, " = ", end="")
    for j in range(len(A[len(A) - 1])):
        if (j != len(A[len(A) - 1]) - 1):

            print_summand(A[len(A) - 1][j], 1)
        else:
            print_summand(A[len(A) - 1][j], 0)

