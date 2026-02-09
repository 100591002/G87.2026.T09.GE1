import re
import json
from .EnterpriseManagementException import EnterpriseManagementException
from .EnterpriseRequest import EnterpriseRequest

class EnterpriseManager:
    def __init__(self):
        pass

    def ValidateCIF( self, CiF ):
        # PLEASE INCLUDE HERE THE CODE FOR VALIDATING THE GUID
        # 1) Basic format: [Letter][7 digits][Control]
        if not isinstance(CiF, str):
            return False

        cif = CiF.strip().upper()
        if not re.fullmatch(r"[A-Z]\d{7}[A-Z0-9]", cif):
            return False

        letter = cif[0]
        digits = cif[1:8]  # 7-digit block
        control = cif[8]  # last char

        # 2) Step 1: sum digits in even positions of the block (positions 2,4,6)
        # positions are 1..7 left-to-right, so indices 1,3,5
        even_sum = int(digits[1]) + int(digits[3]) + int(digits[5])

        # 3) Step 2: odd positions (1,3,5,7) -> multiply by 2, sum digits if needed
        odd_sum = 0
        for idx in (0, 2, 4, 6):
            v = int(digits[idx]) * 2
            odd_sum += (v // 10) + (v % 10)  # digit-sum (0..18)

        # 4) Step 3: partial sum
        partial_sum = even_sum + odd_sum

        # 5) Step 4: base digit
        units = partial_sum % 10
        base_digit = (10 - units) % 10  # handles "if units is 0 -> base digit is 0"

        # 6) Step 5: control character rule + mapping table
        base_to_letter = {0: "J", 1: "A", 2: "B", 3: "C", 4: "D",
                          5: "E", 6: "F", 7: "G", 8: "H", 9: "I"}

        expected_digit = str(base_digit)
        expected_letter = base_to_letter[base_digit]

        # Letter-based rules you provided
        if letter in ("A", "B", "E", "H"):
            return control == expected_digit

        if letter in ("K", "P", "Q", "S"):
            return control == expected_letter

        # For other CIF letters, accept either (common CIF behavior)
        return (control == expected_digit) or (control == expected_letter)
        # RETURN TRUE IF THE GUID IS RIGHT, OR FALSE IN OTHER CASE

    def ReadproductcodefromJSON( self, fi ):

        try:
            with open(fi) as f:
                DATA = json.load(f)
        except FileNotFoundError as e:
            raise EnterpriseManagementException("Wrong file or file path") from e
        except json.JSONDecodeError as e:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from e


        try:
            T_CIF = DATA["cif"]
            T_PHONE = DATA["phone"]
            E_NAME = DATA["enterprise_name"]
            req = EnterpriseRequest(T_CIF, T_PHONE,E_NAME)
        except KeyError as e:
            raise EnterpriseManagementException("JSON Decode Error - Invalid JSON Key") from e
        if not self.ValidateCIF(T_CIF) :
            raise EnterpriseManagementException("Invalid FROM IBAN")
        return req