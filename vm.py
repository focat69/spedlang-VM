import logging, os
logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)

class VMError(Exception): pass
def clear(): os.system('cls' if os.name == 'nt' else 'clear')

TYPES = { # yea i dont ever use this, pointless
    1: 'int',
    2: 'float',
    3: 'string',
    4: 'bool',
    5: 'list',
    6: 'dict',
    7: 'function',
    8: 'class',
    9: 'object',
    10: 'module',
    11: 'file',
    12: 'none',
    13: 'unknown',
}

REVERSED_OPCODES = {
    0x00: 'NOP',
    0x01: 'PUSH',
    0x02: 'POP',
    0x03: 'ADD',
    0x04: 'SUB',
    0x05: 'MUL',
    0x06: 'DIV',
    0x07: 'MOD',
    0x08: 'POW',

    0x09: 'INC',
    0x0A: 'DEC',
    0x0B: 'NEG',
    0x0C: 'POS',

    0x0D: 'AND',
    0x0E: 'OR',
    0x0F: 'XOR',
    0x10: 'NOT',
    0x11: 'SHL',
    0x12: 'SHR',

    0x13: 'EQ',
    0x14: 'NE',
    0x15: 'LT',
    0x16: 'LE',
    0x17: 'GT',
    0x18: 'GE',

    0x19: 'JMP',
    0x1A: 'JE',
    0x1B: 'JNE',
    0x1C: 'JL',
    0x1D: 'JLE',
    0x1E: 'JG',
    0x1F: 'JGE',

    0x20: 'CALL',
    0x21: 'RET',

    0x27: 'LOADK', # constant
    0x28: 'LOADG', # global
    0x29: 'STOREG',
    0x2A: 'STOREK',
}

OPCODES = {v: k for k, v in REVERSED_OPCODES.items()}

class VM:
    def __init__(self):
        self.stack = []
        self.ip = 0
        self.code = []
        self.globals = {}
        self.locals = {}
        self.constants = []

    def push(self, value):
        self.stack.append(value)
        logging.debug(f'PUSH: {value}, STACK: {self.stack}')

    def pop(self):
        if not self.stack:
            raise VMError("Attempt to pop from an empty stack")
        value = self.stack.pop()
        logging.debug(f'POP: {value}, STACK: {self.stack}')
        return value

    def run(self):
        while self.ip < len(self.code):
            opcode = self.code[self.ip]
            self.ip += 1
            logging.debug(f'EXECUTE: {REVERSED_OPCODES.get(opcode, opcode)}, IP: {self.ip}')
            if opcode == OPCODES['NOP']:
                pass
            elif opcode == OPCODES['PUSH']:
                value = self.code[self.ip]
                self.ip += 1
                self.push(value)
            elif opcode == OPCODES['POP']:
                self.pop()
            elif opcode == OPCODES['ADD']:
                self.push(self.pop() + self.pop())
            elif opcode == OPCODES['SUB']:
                self.push(self.pop() - self.pop())
            elif opcode == OPCODES['MUL']:
                self.push(self.pop() * self.pop())
            elif opcode == OPCODES['DIV']:
                self.push(self.pop() / self.pop())
            elif opcode == OPCODES['MOD']:
                self.push(self.pop() % self.pop())
            elif opcode == OPCODES['POW']:
                self.push(self.pop() ** self.pop())
            elif opcode == OPCODES['INC']:
                self.push(self.pop() + 1)
            elif opcode == OPCODES['DEC']:
                self.push(self.pop() - 1)
            elif opcode == OPCODES['NEG']:
                self.push(-self.pop())
            elif opcode == OPCODES['POS']:
                self.push(+self.pop())
            elif opcode == OPCODES['AND']:
                self.push(self.pop() & self.pop())
            elif opcode == OPCODES['OR']:
                self.push(self.pop() | self.pop())
            elif opcode == OPCODES['XOR']:
                self.push(self.pop() ^ self.pop())
            elif opcode == OPCODES['NOT']:
                self.push(~self.pop())
            elif opcode == OPCODES['SHL']:
                self.push(self.pop() << self.pop())
            elif opcode == OPCODES['SHR']:
                self.push(self.pop() >> self.pop())
            elif opcode == OPCODES['EQ']:
                self.push(self.pop() == self.pop())
            elif opcode == OPCODES['NE']:
                self.push(self.pop() != self.pop())
            elif opcode == OPCODES['LT']:
                self.push(self.pop() < self.pop())
            elif opcode == OPCODES['LE']:
                self.push(self.pop() <= self.pop())
            elif opcode == OPCODES['GT']:
                self.push(self.pop() > self.pop())
            elif opcode == OPCODES['GE']:
                self.push(self.pop() >= self.pop())
            elif opcode == OPCODES['JMP']:
                self.ip = self.code[self.ip]
            elif opcode == OPCODES['JE']:
                if self.pop():
                    self.ip = self.code[self.ip]
                else:
                    self.ip += 1
            elif opcode == OPCODES['JNE']:
                if not self.pop():
                    self.ip = self.code[self.ip]
                else:
                    self.ip += 1
            elif opcode == OPCODES['JL']:
                if self.pop() < self.pop():
                    self.ip = self.code[self.ip]
                else:
                    self.ip += 1
            elif opcode == OPCODES['JLE']:
                if self.pop() <= self.pop():
                    self.ip = self.code[self.ip]
                else:
                    self.ip += 1
            elif opcode == OPCODES['JG']:
                if self.pop() > self.pop():
                    self.ip = self.code[self.ip]
                else:
                    self.ip += 1
            elif opcode == OPCODES['JGE']:
                if self.pop() >= self.pop():
                    self.ip = self.code[self.ip]
                else:
                    self.ip += 1
            elif opcode == OPCODES['CALL']:
                pass
            elif opcode == OPCODES['RET']:
                pass
            elif opcode == OPCODES['LOADK']:
                value = self.code[self.ip]
                self.ip += 1
                self.push(self.constants[value])
            elif opcode == OPCODES['LOADG']:
                value = self.code[self.ip]
                self.ip += 1
                self.push(self.globals[value])
            elif opcode == OPCODES['STOREG']:
                value = self.code[self.ip]
                self.ip += 1
                self.globals[value] = self.pop()
            elif opcode == OPCODES['STOREK']:
                index = self.code[self.ip]
                self.ip += 1
                self.constants[index] = self.pop()
            else:
                raise VMError(f'Unknown opcode: {opcode}')
            
    def disassemble(self):
        i = 0
        while i < len(self.code):
            opcode = self.code[i]
            if opcode in REVERSED_OPCODES:
                if opcode in {OPCODES['LOADK'], OPCODES['STOREK'], OPCODES['LOADG'], OPCODES['STOREG']}:
                    print(f'{i:04x}: {REVERSED_OPCODES[opcode]} K{self.code[i+1]} = {self.constants[self.code[i+1]]}')
                    i += 2
                else:
                    print(f'{i:04x}: {REVERSED_OPCODES[opcode]}')
                    i += 1
            else:
                print(f'{i:04x}: {opcode}')
                i += 1

    def interpret(self):
        self.run()
        return self.stack

if __name__ == '__main__':
    tests = {
        "t1": {
            "result": [3],
            "output": None,
            "code": [
                OPCODES['LOADK'], 0, # k0 = 1
                OPCODES['LOADK'], 1, # k1 = 2
                OPCODES['ADD'], # k0 + k1
            ],
            "constants": [1, 2, 0],
            "passed": False
        },
        "t2": {
            "result": [72],
            "output": None,
            "code": [
                OPCODES['LOADK'], 0, # k0 = 1
                OPCODES['LOADK'], 1, # k1 = 2
                OPCODES['ADD'], # k0 + k1
                OPCODES['STOREK'], 2, # store result in k2
                OPCODES['LOADK'], 2, # load k2 (result -> k0 + k1)
                OPCODES['LOADK'], 3, # k3 = 69
                OPCODES['ADD'], # k2 + k3
            ],
            "constants": [1, 2, 0, 69, 0],
            "passed": False
        },
        "t3": {
            "result": [492],
            "output": None,
            "code": [
                OPCODES['LOADK'], 0, # k0 = 1
                OPCODES['LOADK'], 1, # k1 = 2
                OPCODES['ADD'], # k0 + k1
                OPCODES['STOREK'], 2, # store result in k2
                OPCODES['LOADK'], 2, # load k2 (result -> k0 + k1)
                OPCODES['LOADK'], 3, # k3 = 69
                OPCODES['ADD'], # k2 + k3
                OPCODES['STOREK'], 4, # store result in k4
                OPCODES['LOADK'], 4, # load k4 (result -> k2 + k3)
                OPCODES['LOADK'], 5, # k5 = 420
                OPCODES['ADD'], # k4 + k5
            ],
            "constants": [1, 2, 0, 69, 0, 420, 0],
            "passed": False
        },

        "t4": {
            "result": [15],
            "output": None,
            "code": [
                OPCODES['LOADK'], 0, # k0 = 5
                OPCODES['LOADK'], 1, # k1 = 3
                OPCODES['MUL'], # k0 * k1
            ],
            "constants": [5, 3, 0],
            "passed": False
        },
        "t5": {
            "result": [ 3 / 6 ],
            "output": None,
            "code": [
                OPCODES['LOADK'], 0, # k0 = 6
                OPCODES['LOADK'], 1, # k1 = 3
                OPCODES['DIV'], # k0 / k1
            ],
            "constants": [6, 3, 0],
            "passed": False
        },

        "t6": {
            "result": [ 3 % 6 ],
            "output": None,
            "code": [
                OPCODES['LOADK'], 0, # k0 = 6
                OPCODES['LOADK'], 1, # k1 = 3
                OPCODES['MOD'], # k0 % k1
            ],
            "constants": [6, 3, 0],
            "passed": False
        },
        "t7": {
            "result": [ 3 ** 5 ],
            "output": None,
            "code": [
                OPCODES['LOADK'], 0, # k0 = 5
                OPCODES['LOADK'], 1, # k1 = 3
                OPCODES['POW'], # k0 ** k1
            ],
            "constants": [5, 3, 0],
            "passed": False
        },

        "t8": {
            "result": [6],
            "output": None,
            "code": [
                OPCODES['LOADK'], 0, # k0 = 5
                OPCODES['INC'], # k0 + 1
            ],
            "constants": [5, 0],
            "passed": False
        },
        "t9": {
            "result": [4],
            "output": None,
            "code": [
                OPCODES['LOADK'], 0, # k0 = 5
                OPCODES['DEC'], # k0 - 1
            ],
            "constants": [5, 0],
            "passed": False
        },
        
        "t10": {
            "result": [-5],
            "output": None,
            "code": [
                OPCODES['LOADK'], 0, # k0 = 5
                OPCODES['NEG'], # -k0
            ],
            "constants": [5, 0],
            "passed": False
        },
        "t11": {
            "result": [5],
            "output": None,
            "code": [
                OPCODES['LOADK'], 0, # k0 = 5
                OPCODES['POS'], # +k0
            ],
            "constants": [5, 0],
            "passed": False
        },

        "t12": {
            "result": [6 & 6],
            "output": None,
            "code": [
                OPCODES['LOADK'], 0, # k0 = 6
                OPCODES['LOADK'], 1, # k1 = 6
                OPCODES['AND'], # k0 & k1
            ],
            "constants": [6, 6, 0],
            "passed": False
        },

        "t13": {
            "result": [3],
            "output": None,
            "code": [
                OPCODES['LOADK'], 0, # k0 = 1
                OPCODES['LOADK'], 1, # k1 = 2
                OPCODES['OR'], # k0 | k1
            ],
            "constants": [1, 2, 0],
            "passed": False
        },

        "t14": {
            "result": [3],
            "output": None,
            "code": [
                OPCODES['LOADK'], 0, # k0 = 1
                OPCODES['LOADK'], 1, # k1 = 2
                OPCODES['XOR'], # k0 ^ k1
            ],
            "constants": [1, 2, 0],
            "passed": False
        },

    }

    for test_name, test in tests.items():
        clear()
        print(f"[ {test_name} ]")
        vm = VM()
        vm.code = test["code"]
        vm.constants = test["constants"]

        output = vm.interpret()
        test["output"] = output
        print(output)

        vm.disassemble()
        if output == test["result"]:
            print(f"[✔] {test_name} -> passed")
            test["passed"] = True
        else:
            print(f"[✘] {test_name} -> failed")
        
        if test_name == list(tests.keys())[-1]:
            input('[/] press enter to show summary...')
        else:
            input('[/] press enter to go to the next test...')

    clear()
    with open('output.txt', 'w', encoding='utf-8') as f:
        print("[ SUMMARY ]")
        f.write("[ SUMMARY ]\n")
        print("Formatted as:\n[✔] test_name\n    -> R: result / O: output\n")
        f.write("Formatted as:\n[✔] test_name\n    -> R: result / O: output\n\n")
        for test_name, test in tests.items():
            print(f"[{'✔' if test['passed'] else '✘'}] {test_name}\n    -> R: {test['result']} / O: {test['output']}")
            f.write(f"[{'✔' if test['passed'] else '✘'}] {test_name}\n    -> R: {test['result']} / O: {test['output']}\n")

    print("\n[✔] output.txt file created.")
    input('[/] press enter to exit...')
