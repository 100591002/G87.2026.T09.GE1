import re
import json
from .EnterpriseManagementException import EnterpriseManagementException
from .EnterpriseRequest import EnterpriseRequest

class EnterpriseManager:
    """
    Manages enterprise-related operations such as CIF validation
    and request creation from JSON input.
    """
    def __init__(self):
        pass

    def ValidateCIF( self, CiF ):
        """
        Validate a CIF identifier.

        Returns True if the CIF is valid according to format and
        checksum rules, otherwise False.
        """
        # PLEASE INCLUDE HERE THE CODE FOR VALIDATING THE GUID
        # 1) Basic format: [Letter][7 digits][Control]
        if not isinstance(CiF, str):
            return False

        CIF = CiF.strip().upper()
        if not re.fullmatch(r"[A-Z]\d{7}[A-Z0-9]", CIF):
            return False

        LETTER = CIF[0]
        DIGITS = CIF[1:8]  # 7-digit block
        CONTROL = CIF[8]  # last char

        # 2) Step 1: sum digits in even positions of the block (positions 2,4,6)
        # positions are 1..7 left-to-right, so indices 1,3,5
        EVEN_SUM = int(DIGITS[1]) + int(DIGITS[3]) + int(DIGITS[5])

        # 3) Step 2: odd positions (1,3,5,7) -> multiply by 2, sum digits if needed
        ODD_SUM = 0
        for IDX in (0, 2, 4, 6):
            V = int(DIGITS[IDX]) * 2
            ODD_SUM += (V // 10) + (V % 10)  # digit-sum (0..18)

        # 4) Step 3: partial sum
        PARTIAL_SUM = EVEN_SUM + ODD_SUM

        # 5) Step 4: base digit
        UNITS = PARTIAL_SUM % 10
        BASE_DIGIT = (10 - UNITS) % 10  # handles "if units is 0 -> base digit is 0"

        # 6) Step 5: control character rule + mapping table
        BASE_TO_LETTER = {0: "J", 1: "A", 2: "B", 3: "C", 4: "D",
                          5: "E", 6: "F", 7: "G", 8: "H", 9: "I"}

        EXPECTED_DIGIT = str(BASE_DIGIT)
        EXPECTED_LETTER = BASE_TO_LETTER[BASE_DIGIT]

        # Letter-based rules you provided
        if LETTER in ("A", "B", "E", "H"):
            return CONTROL == EXPECTED_DIGIT

        if LETTER in ("K", "P", "Q", "S"):
            return CONTROL == EXPECTED_LETTER

        # For other CIF letters, accept either (common CIF behavior)
        return (CONTROL == EXPECTED_DIGIT) or (CONTROL == EXPECTED_LETTER)
        # RETURN TRUE IF THE GUID IS RIGHT, OR FALSE IN OTHER CASE

    def ReadproductcodefromJSON( self, fi ):
        """
        Read enterprise data from a JSON file and return an
        EnterpriseRequest object.

        Raises EnterpriseManagementException if the file is invalid
        or contains incorrect data.
        """

        try:
            with open(fi) as F:
                DATA = json.load(F)
        except FileNotFoundError as E:
            raise EnterpriseManagementException("Wrong file or file path") from E
        except json.JSONDecodeError as E:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from E


        try:
            T_CIF = DATA["cif"]
            T_PHONE = DATA["phone"]
            E_NAME = DATA["enterprise_name"]
            REQ = EnterpriseRequest(T_CIF, T_PHONE,E_NAME)
        except KeyError as E:
            raise EnterpriseManagementException("JSON Decode Error - Invalid JSON Key") from E
        if not self.ValidateCIF(T_CIF) :
            raise EnterpriseManagementException("Invalid FROM IBAN")
        return REQ