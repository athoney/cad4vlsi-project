import unittest
from qm import (
    combine_terms,
    generate_prime_implicants,
    solve_prime_implicant_table,
    quine_mccluskey,
    read_pla_file,
    __main__,
    expand_terms
)

class TestQuineMcCluskey(unittest.TestCase):

    def test_combine_terms(self):
        self.assertEqual(combine_terms('0001', '0011'), '00-1')
        self.assertEqual(combine_terms('1010', '1000'), '10-0')
        self.assertEqual(combine_terms('1110', '1111'), '111-')
        self.assertEqual(combine_terms('1111111101111', '1101111101111'), '11-1111101111')
        self.assertIsNone(combine_terms('00', '11'))  # More than one bit difference
        self.assertIsNone(combine_terms('10', '10'))  # No difference


    def test_generate_prime_implicantsB2(self):
        minterms = ['00', '01', '10']
        expected_primes = ['0-', '-0']
        result = generate_prime_implicants(minterms)
        self.assertCountEqual(result, expected_primes)

    def test_generate_prime_implicantsB3(self):
        minterms = ['000', '001', '111', '101']
        expected_primes = ['00-', '-01', '1-1']
        result = generate_prime_implicants(minterms)
        self.assertCountEqual(result, expected_primes)

    def test_generate_prime_implicantsB4(self):
        minterms = ['1000', '1010', '1011', '0111', '1111']
        expected_primes = ['10-0', '101-', '-111', '1-11']
        result = generate_prime_implicants(minterms)
        self.assertCountEqual(result, expected_primes)
    
    def test_generate_prime_implicantsB5(self):
        minterms = ['00000', '00001', '00010', '00100', '01000', '10000', '00101', '01001', '10001', '10010', '10100', '11000', '01011', '01101', '01110', '10011', '11001']
        expected_primes = [ '-00-0', '01110', '100--', '--00-',  '00-0-', '0--01', '010-1', '-0-00']
        result = generate_prime_implicants(minterms)
        self.assertCountEqual(result, expected_primes)

    def test_generate_prime_implicantsB6(self):
        minterms = ['000000', '000100','001101', '001111', '111111']
        expected_primes = ['000-00', '0011-1', '111111']
        result = generate_prime_implicants(minterms)
        self.assertCountEqual(result, expected_primes)

    def test_solve_prime_implicantsB2(self):
        minterms = ['00', '01', '10']
        expected_primes = ['0-', '-0']
        expected_solution = ['0-', '-0']
        result = solve_prime_implicant_table(expected_primes, minterms)
        self.assertCountEqual(result, expected_solution)

    def test_solve_prime_implicantsB3(self):
        minterms = ['000', '001', '111', '101']
        expected_primes = ['00-', '-01', '1-1']
        expected_solution = ['00-', '1-1']
        result = solve_prime_implicant_table(expected_primes, minterms)
        self.assertCountEqual(result, expected_solution)

    def test_solve_prime_implicantsB4(self):
        minterms = ['1000', '1010', '1011', '0111', '1111']
        expected_primes = ['10-0', '101-', '-111', '1-11']
        expected_solution = ['-111', '10-0', '101-']
        result = solve_prime_implicant_table(expected_primes, minterms)
        self.assertCountEqual(result, expected_solution)

    def test_solve_prime_implicantsB5(self):
        minterms = ['00000', '00001', '00010', '00100', '01000', '10000', '00101', '01001', '10001', '10010', '10100', '11000', '01011', '01101', '01110', '10011', '11001']
        expected_primes = [ '-00-0', '01110', '100--', '--00-',  '00-0-', '0--01', '010-1', '-0-00']
        expected_solution = ['--00-', '-00-0', '-0-00', '0--01', '100--', '010-1','01110']
        result = solve_prime_implicant_table(expected_primes, minterms)
        self.assertCountEqual(result, expected_solution)

    def test_solve_prime_implicantsB6(self):
        minterms = ['000000', '000100','001101', '001111', '111111']
        expected_primes = ['000-00', '0011-1', '111111']
        expected_solution = ['000-00', '0011-1', '111111']
        result = solve_prime_implicant_table(expected_primes, minterms)
        self.assertCountEqual(result, expected_solution)

    def test_quine_mccluskeyB2(self):
        minterms = ['00', '01', '10']
        expected_solution = ['0-', '-0']
        result = quine_mccluskey(minterms)
        self.assertCountEqual(result, expected_solution)

    def test_quine_mccluskeyB3(self):
        minterms = ['000', '001', '111', '101']
        expected_solution = ['00-', '1-1']
        result = quine_mccluskey(minterms)
        self.assertCountEqual(result, expected_solution)

    def test_quine_mccluskeyB4(self):
        minterms = ['1000', '1010', '1011', '0111', '1111']
        expected_solution = ['-111', '10-0', '101-']
        result = quine_mccluskey(minterms)
        self.assertIn(sorted(result), [sorted(expected_solution), sorted(['-111', '1-11', '10-0'])])

    def test_quine_mccluskeyB4dc(self):
        minterms = ['0000', '0101', '1100', '1001']
        dc = ['0001', '0100', '1101', '1000']
        expected_solution = ['--0-']
        result = quine_mccluskey(minterms,dc)
        self.assertCountEqual(result, expected_solution)

    def test_quine_mccluskeyB5(self):
        minterms = ['00000', '00001', '00010', '00100', '01000', '10000', '00101', '01001', '10001', '10010', '10100', '11000', '01011', '01101', '01110', '10011', '11001']
        expected_solution = ['--00-', '-00-0', '-0-00', '0--01', '100--', '010-1','01110']
        result = quine_mccluskey(minterms)
        self.assertCountEqual(result, expected_solution)
    
    def test_quine_mccluskeyB6(self):
        minterms = ['000000', '000100','001101', '001111', '111111']
        expected_solution = ['000-00', '0011-1', '111111']
        result = quine_mccluskey(minterms)
        self.assertCountEqual(result, expected_solution)

    def test_qm8(self):
        inputfile = "./input_examples/8inputs.pla"
        inputs = read_pla_file(inputfile)
        outputs = read_pla_file('./output_examples/i8eqn.pla')['p']
        minterms = inputs["terms"]["1"]
        dc = inputs["terms"]["-"]
        minimized = __main__(inputfile)
        onset = expand_terms(minimized)

        # Check if the minterms are a subset of the onset terms
        self.assertTrue(set(minterms).issubset(set(onset)))
        # Check that any minterm not covered by the onset terms is a don't care  
        self.assertTrue((set(minterms).difference(set(onset))).issubset(set(dc)))
        # Check that the number of implicants in the minized function is equal to the number of implicants in the output file
        self.assertEqual(len(minimized), outputs)

    def test_qm9(self):
        inputfile = "./input_examples/9inputs.pla"
        inputs = read_pla_file(inputfile)
        outputs = read_pla_file('./output_examples/i9eqn.pla')['p']
        minterms = inputs["terms"]["1"]
        dc = inputs["terms"]["-"]
        minimized = __main__(inputfile)
        onset = expand_terms(minimized)

        # Check if the minterms are a subset of the onset terms
        self.assertTrue(set(minterms).issubset(set(onset)))
        # Check that any minterm not covered by the onset terms is a don't care  
        self.assertTrue((set(minterms).difference(set(onset))).issubset(set(dc)))
        # Check that the number of implicants in the minized function is equal to the number of implicants in the output file
        self.assertEqual(len(minimized), outputs)

    def test_qm10(self):
        inputfile = "./input_examples/10inputs.pla"
        inputs = read_pla_file(inputfile)
        outputs = read_pla_file('./output_examples/i10eqn.pla')['p']
        minterms = inputs["terms"]["1"]
        dc = inputs["terms"]["-"]
        minimized = __main__(inputfile)
        onset = expand_terms(minimized)

        # Check if the minterms are a subset of the onset terms
        self.assertTrue(set(minterms).issubset(set(onset)))
        # Check that any minterm not covered by the onset terms is a don't care  
        self.assertTrue((set(minterms).difference(set(onset))).issubset(set(dc)))
        # Check that the number of implicants in the minized function is equal to the number of implicants in the output file
        self.assertEqual(len(minimized), outputs)

    def test_expand_terms1(self):
        terms = ['1-1', '1-0']
        expected_result = ['101', '111', '100', '110']
        result = expand_terms(terms)
        self.assertCountEqual(result, expected_result)

    


if __name__ == '__main__':
    unittest.main()
