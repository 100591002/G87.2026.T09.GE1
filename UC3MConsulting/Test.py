from  .EnterpriseManager import EnterpriseManager

em = EnterpriseManager()

EXAMPLES = [
    "B12345674",  # might be True or False depending on control
    "A00003450",
    "P2345678H",
    "B1234567X",  # invalid control
    "123",        # invalid format
    None,         # invalid type
]

for e in EXAMPLES:
    print(e, "->", em.ValidateCIF(e))
