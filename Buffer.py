from Record import Record
from Sign import Sign
from Record import RECORD_SIZE


class Buffer:
    read_counter = 0
    write_counter = 0

    def __init__(self, file_in, file_b, file_c, value_file, name):
        self._name = name
        self._read_file = file_in
        self._file_B = file_b
        self._file_C = file_c
        self._value_file = value_file
        self._MAX_SIZE = 100
        self._current_size = 0
        self._buffer = []
        self._direction = 'B'
        # self.record_num = 0

    def write_page(self):
        for _ in range(self._MAX_SIZE):
            record = []
            byte = self.read_from_file()
            if byte != b'':
                record.append(Sign(byte))
                for i in range(RECORD_SIZE-1):
                    byte = self.read_from_file()
                    if byte != b'':
                        record.append(Sign(byte))
                    else:
                        raise ValueError('record not complete?')
            if len(record) != 0:
                self._buffer.append(Record(record))
                self._current_size += 1
        if self._current_size != 0:
            Buffer.read_counter += 1

    def save_page(self):
        if self._current_size != 0:
            Buffer.write_counter += 1
        if self._name == 'B':
            for l in range(self._current_size):
                for i in range(RECORD_SIZE):
                    self._file_B.write(self._buffer[l].sign_list[i].get_sign())
        elif self._name == 'C':
            for l in range(self._current_size):
                for i in range(RECORD_SIZE):
                    self._file_C.write(self._buffer[l].sign_list[i].get_sign())
        elif self._name == 'D':
            for l in range(self._current_size):
                for i in range(RECORD_SIZE):
                    self._read_file.write(self._buffer[l].sign_list[i].get_sign())
                self._value_file.write(str(self._buffer[l].get_value()))
                self._value_file.write(' ')
        else:
            raise ValueError('this buffer doesnt save pages')
        self._current_size = 0
        self._buffer.clear()

    def read_record(self):
        if self._current_size != 0:
            record = self._buffer[0]
            self._current_size -= 1
            self._buffer.pop(0)
            if self._current_size == 0:
                self.write_page()
            return record
        elif self._current_size == 0:  # and self._name == 'A'
            self.write_page()
            if self._current_size != 0:
                record = self._buffer[0]
                self._current_size -= 1
                self._buffer.pop(0)
                return record
        return False

    def write_record(self, record):
        self._buffer.append(record)
        self._current_size += 1
        if self._current_size == self._MAX_SIZE:
            self.save_page()

    def switch_direction(self):
        if self._direction == 'B':
            self._direction = 'C'
        elif self._direction == 'C':
            self._direction = 'B'

    def get_direction(self):
        return self._direction

    def get_size(self):
        return self._current_size

    def get_top_value(self):
        return self._buffer[0].get_value()

    def read_from_file(self):
        if self._name == 'A':
            byte = self._read_file.read(1)
        elif self._name == 'B_out':
            byte = self._file_B.read(1)
        elif self._name == 'C_out':
            byte = self._file_C.read(1)
        return byte