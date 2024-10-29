from itertools import combinations

class Espresso:
    def __init__(self, minterms, num_vars):
        self.minterms = minterms
        self.num_vars = num_vars

    def minimize(self):
        """Run the Espresso minimization."""
        prime_implicants = self.generate_prime_implicants()
        essential_primes = self.find_essential_prime_implicants(prime_implicants)
        return essential_primes

    def generate_prime_implicants(self):
        """Generate prime implicants by combining minterms."""
        groups = self.group_minterms_by_ones(self.minterms)
        prime_implicants = []

        while groups:
            next_groups = {}
            marked = set()
            for i in range(len(groups) - 1):
                for term1 in groups[i]:
                    for term2 in groups[i + 1]:
                        merged = self.merge_terms(term1, term2)
                        if merged:
                            next_groups.setdefault(i, []).append(merged)
                            marked.add(term1)
                            marked.add(term2)
            # Add unmarked terms as prime implicants
            for group in groups.values():
                for term in group:
                    if term not in marked:
                        prime_implicants.append(term)
            groups = next_groups

        return prime_implicants

    def find_essential_prime_implicants(self, prime_implicants):
        """Find essential prime implicants."""
        essential = []
        coverage = {m: [] for m in self.minterms}
        for implicant in prime_implicants:
            for minterm in self.minterms:
                if self.covers(implicant, minterm):
                    coverage[minterm].append(implicant)

        for minterm, implicants in coverage.items():
            if len(implicants) == 1:
                essential.append(implicants[0])

        return list(set(essential))

    def group_minterms_by_ones(self, minterms):
        """Group minterms by the number of 1s."""
        groups = {}
        for minterm in minterms:
            ones = sum(1 for bit in minterm if bit == '1')
            groups.setdefault(ones, []).append(minterm)
        return groups

    def merge_terms(self, term1, term2):
        """Merge two terms if they differ by one bit."""
        diff = sum(1 for a, b in zip(term1, term2) if a != b)
        if diff == 1:
            return ''.join('-' if a != b else a for a, b in zip(term1, term2))
        return None

    def covers(self, implicant, minterm):
        """Check if an implicant covers a minterm."""
        return all(i == '-' or i == m for i, m in zip(implicant, minterm))


# Example usage
if __name__ == "__main__":
    # Define the minterms (in binary) and the number of variables
    minterms = ["000", "001", "111", "010", "110"]
    num_vars = 3

    espresso = Espresso(minterms, num_vars)
    result = espresso.minimize()
    print("Simplified Boolean function (essential prime implicants):", result)
