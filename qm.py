import itertools

def combine_terms(term1, term2):
    """Combine two binary terms if they differ by only one bit."""
    diff_index = -1
    for i, (b1, b2) in enumerate(zip(term1, term2)):
        if b1 != b2:
            if diff_index != -1:  # More than one difference
                return None
            diff_index = i
    if diff_index == -1:  # No differences
        return None
    return term1[:diff_index] + '-' + term1[diff_index + 1:]

def generate_prime_implicants(minterms):
    """Generate the prime implicants from the given minterms."""
    # separate the minterms into groups based on hamming weight
    groups = {}
    for minterm in minterms:
        count_ones = minterm.count('1')
        groups.setdefault(count_ones, []).append(minterm)

    prime_implicants = set()
    used = set()
    while groups:
        new_groups = {}
        for i in sorted(groups.keys()):
            if i + 1 not in groups:
                continue
            for term1 in groups[i]:
                for term2 in groups[i + 1]:
                    combined = combine_terms(term1, term2)
                    if combined:
                        used.add(term1)
                        used.add(term2)
                        count_ones = combined.count('1')
                        new_groups.setdefault(count_ones, []).append(combined)
        # Add terms that were not combined to the prime implicants
        for terms in groups.values():
            for term in terms:
                if term not in used:
                    prime_implicants.add(term)
        groups = new_groups
    return list(prime_implicants)

def solve_prime_implicant_table(prime_implicants, minterms):
    from itertools import combinations

    # Step 1: Build the coverage table
    coverage = {implicant: set() for implicant in prime_implicants}
    for implicant in prime_implicants:
        for minterm in minterms:
            if matches(implicant, minterm):
                coverage[implicant].add(minterm)

    # Step 2: Identify essential prime implicants
    essential = set()
    uncovered = set(minterms)
    for minterm in minterms:
        covers = [pi for pi in prime_implicants if minterm in coverage[pi]]
        if len(covers) == 1:  # Only one PI covers this minterm
            essential.add(covers[0])

    # Remove covered minterms
    for e in essential:
        uncovered -= coverage[e]

    # Step 3: Minimize remaining coverage
    remaining_pis = [pi for pi in prime_implicants if pi not in essential]
    best_solution = essential.copy()

    if uncovered:
        # Generate all subsets of remaining PIs to find the minimal solution
        minimal_cover = None
        for r in range(1, len(remaining_pis) + 1):
            for subset in combinations(remaining_pis, r):
                # Check if this subset covers all remaining uncovered minterms
                subset_cover = set.union(*(coverage[pi] for pi in subset))
                if uncovered.issubset(subset_cover):
                    if minimal_cover is None or len(subset) < len(minimal_cover):
                        minimal_cover = set(subset)
            if minimal_cover:
                break  # Stop as soon as we find the smallest cover

        if minimal_cover:
            best_solution.update(minimal_cover)

    return best_solution


def matches(implicant, minterm):
    """Check if a prime implicant matches a minterm."""
    return all(i == m or i == '-' for i, m in zip(implicant, minterm))


def quine_mccluskey(minterms, dc=[]):
    """Full Quine-McCluskey method for minimizing boolean functions."""
    prime_implicants = generate_prime_implicants(minterms+dc)
    return solve_prime_implicant_table(prime_implicants, minterms)

def read_pla_file(filepath):
    pla_data = {"inputs": 0, "outputs": 0, "terms": {'1': [], '-': []}}
    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith(".i "):
                pla_data["inputs"] = int(line.split()[1])
            elif line.startswith(".o "):
                pla_data["outputs"] = int(line.split()[1])
            elif line.startswith(".ilb"):
                pla_data["input_labels"] = line.split()[1:]
            elif line.startswith(".ob"):
                pla_data["output_labels"] = line.split()[1]
            elif line.startswith(".p "):
                pla_data["p"] = int(line.split()[1])
            elif not line.startswith(".") and not line.startswith("#"):
                term = line.split()
                pla_data["terms"][str(term[1])].append(term[0])
    return pla_data


def generate_pla(input_labels, output_label, minimized_terms, filename):
    with open(filename, 'w') as f:
        # Write header
        f.write(f".i {len(input_labels)}\n")
        f.write(f".o {len(output_label)}\n")
        f.write(f".ilb {' '.join(input_labels)}\n")
        f.write(f".ob {output_label}\n")
        f.write(f".p {len(minimized_terms)}\n")
        
        # Write terms
        for term in minimized_terms:
            f.write(f"{term} 1\n")
        
        # Write end marker
        f.write(".e\n")


def expand_terms(terms):
    """Test helper function ; Expand terms with '-' to all possible combinations."""
    expanded = []
    for term in terms:
        # Generate all combinations for the positions of '-'
        expanded.extend([
            ''.join(bits)
            for bits in itertools.product(
                *[('0', '1') if char == '-' else (char,) for char in term]
            )
        ])
    return expanded



def __main__(filename=None):
    if filename:
        pla_file = filename
    else:
        pla_file = input("Enter a filename: ")
    pla_content = read_pla_file(pla_file)
    minimized = quine_mccluskey(pla_content["terms"]["1"], pla_content["terms"]["-"])
    generate_pla(pla_content["input_labels"], pla_content["output_labels"], minimized, f"{pla_content['inputs']}output.pla")
    # print(minimized)
    return minimized

    



# __main__()
