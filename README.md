# cad4vlsi-project

## Project Description
This project is a part of the course CAD for VLSI Design. This project implements the Quine-McCluskey algorithm for minimization of boolean functions and utilizes petrick's minimization algorithm to find the minimal solution. The project is implemented in Python.

## Notes
- Since Petrick's method is used to find the minimal solution, the output may vary between runs if two solutions are equally optimal. For example, the test: test_quine_mccluskeyB4 will have two possible minimal solutions.
- This code can handle an onset with don't cares.

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