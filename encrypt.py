#! /usr/bin/env python

import re

class Encryptor:
    elements_dict = {
        "a": "u3Y$", "b": "+b0P", "c": "~Cp6", "d": "O^d8", "e": "^e5B",
        "f": "Rw4~", "g": "n2N^", "h": "c@T8", "i": "_dG6", "j": "9G&o",
        "k": "w+W3", "l": "Gx@4", "m": "L4b@", "n": "+3zI", "o": "O6r!",
        "p": "D2p#", "q": "Wg&3", "r": "3Jj&", "s": "E6&e", "t": "X~3g",
        "u": "^eO6", "v": "J4+o", "w": "h@6K", "x": "q#W4", "y": "Bm5^",
        "z": "+3Ip"
    }

    d_inversion = {'~': '1', '!': '2', '@': '3', '#': '4', '$': '5', '^': '6', '&': '7', '*': '8', '_': '9', '+': '0'}
    d_keys = tuple(d_inversion.keys())
    d_numbers = tuple(d_inversion.values())

    def __init__(self, hint):
        self.hint = hint
        self.p_sh = hint.index('#')
        self.p_ex = hint.index('@')
        self.p_in = hint.index('$')
        self.hint_w_tn = self._strip_hint()
        self.hint_tuple = tuple([i for i in self.hint_w_tn])
        self.pc = self._get_pc()

    def _strip_hint(self):
        hint_w_tn = self.hint.replace('#', '').replace('@', '').replace('$', '')
        hint_w_tn = re.sub(r'\d+', '', hint_w_tn)
        return hint_w_tn

    def _get_pc(self):
        return ''.join([self.elements_dict[i] for i in self.hint_tuple])

    def _sh_pc(self):
        all_sh = (
            (0, 1, 3, 2), (1, 0, 3, 2), (2, 1, 0, 3), (0, 3, 1, 2),
            (1, 0, 2, 3), (3, 0, 2, 1), (3, 2, 0, 1), (0, 2, 3, 1)
        )
        sh_method = tuple(all_sh[self.p_sh])
        self.hint_tuple = tuple(self.hint_tuple[sh_method[i]] for i in range(4))

    def _ex_pc(self):
        if self.p_ex in (0, 1):
            ex_method = 0
        elif self.p_ex in (2, 3):
            ex_method = 1
        elif self.p_ex in (4, 5):
            ex_method = 2
        else:
            ex_method = 3

        def get_value(i):
            return self.elements_dict[self.hint_tuple[i]]

        ex_str = ''.join([get_value(i)[ex_method] for i in range(4)])
        str_ex_pc = ''.join([get_value(i).replace(get_value(i)[ex_method], '') for i in range(4)])

        self.pc = str_ex_pc + ex_str

    def _in_pc(self):
        new_pc = ''
        for i in range(16):
            if self.pc[i].isupper():
                new_pc += self.pc[i].lower()
            elif self.pc[i].islower():
                new_pc += self.pc[i].upper()
            elif self.pc[i] in self.d_numbers:
                index = self.d_numbers.index(self.pc[i])
                new_pc += self.d_keys[index]
            elif self.pc[i] in self.d_keys:
                index = self.d_keys.index(self.pc[i])
                new_pc += str(self.d_numbers[index])
        self.pc = new_pc

    def encrypt(self):
        self._sh_pc()
        self.pc = self._get_pc()
        self._ex_pc()
        self._in_pc()
        print(self.pc)
        return self.pc

if __name__ == "__main__":
	hint_input = input('Enter the hint: ')
	encryptor = Encryptor(hint_input)
	encryptor.encrypt()