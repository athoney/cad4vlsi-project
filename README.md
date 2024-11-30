# cad4vlsi-project

## Project Description
This project is a part of the course CAD for VLSI Design. This project implements the Quine-McCluskey algorithm for minimization of boolean functions and utilizes petrick's minimization algorithm to find the minimal solution. The project is implemented in Python.

## Notes
- Since Petrick's method is used to find the minimal solution, the output may vary between runs if two solutions are equally optimal. For example, the test: test_quine_mccluskeyB4 will have two possible minimal solutions.
- This code can handle an onset with don't cares.

## Verification
The project has been verified using the `test_qm.py` file. Each individual function has been tested at length. Additionally, the project has been tested with `test_qm#.py` unit tests. The test cases ensure the the Quine-McCluskey algorithm produces an equation that appropriately covers the onset from the input with the following lines:
```python
self.assertTrue(set(minterms).issubset(set(onset)))
self.assertTrue((set(minterms).difference(set(onset))).issubset(set(dc)))
```
Moreover, I ensure the equation is minimal by checking the number of generated implicants against a known minimal solution (generated on the Eustisis server with abc). The test cases are as follows:
```python
self.assertEqual(len(minimized), outputs)
```
It should be noted one of the tests fail. My code found a solution that uses one less implicant than the abc solution.

## Usage:
1. Run `qm.py`
2. Enter the filepath to your pla file
3. The minimized output will appear in output.pla

## Example:
```bash
$ python qm.py
Enter a filename: ex.pla
$ cat output.pla
```