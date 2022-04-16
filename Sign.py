class Sign:
    def __init__(self, sign):
        self._sign = sign
        self._asci_val = ord(sign)
        self._ones_amount = bin(self._asci_val).count("1")

    def count_ones(self):
        print(self._ones_amount)

    def get_sign(self):
        return self._sign

    def get_ones_amount(self):
        return self._ones_amount
