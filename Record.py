RECORD_SIZE = 10


class Record:
    def __init__(self, sign_list):
        self.sign_list = sign_list
        temp = 0
        for sign in sign_list:
            temp += sign.get_ones_amount()
        self._value = temp

    def get_value(self):
        return self._value
