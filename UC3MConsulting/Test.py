"""
Example script demonstrating CIF validation using EnterpriseManager.

This module creates an EnterpriseManager instance and validates
several sample CIF values, printing the results to standard output.
"""

from  .EnterpriseManager import EnterpriseManager

em = EnterpriseManager()

EXAMPLES = [
    "B12345674",  # True
    "A00003450",  # False -- the expected control digit is 9 instead of 0
    "P2345678H",  # False -- the expected control number is C instead of H
    "B1234567X",  # False -- B requires a digit control, not a letter
    "123",        # False -- invalid format
    None,         # False -- invalid type
]

for e in EXAMPLES:
    print(e, "->", em.ValidateCIF(e))
