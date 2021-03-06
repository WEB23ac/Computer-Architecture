"""CPU functionality."""

import sys
from commands import *


# class CommandInterpreter:

#     def __init__(self):
#         self.create_branchtable()

#     def create_branchtable(self):
#         self.branchtable = {}
#         filename = 'commands.py'
#         with open(filename) as f:
#             for line in f:
#                 cmt_split = line.split('=')
#                 cmd_name = cmt_split[0].stri()
#                 cmd_value = cmt_split[1].replace('\n', '')

#             name_function = 'handle_' + cmd_name
#             function = getattr(self, name_function)
#             self.branchtable[int(cmd_value, 2)] = function

#     def handle_LDI(self, a, b):
#         reg_a = self.ram_read(a)
#         reb_b = self.ram_read(b)
#         self.register[reg_a] = reb_b
#         self.pc += 3

#     def handle_PRN(self, a, b):
#         reg_a = self.ram_read(a)
#         res = self.register[reg_a]
#         print(res)

#     def handle_MUL(self, a, b):
#         reg_a = self.ram_read(a)
#         reg_b = self.ram_read(b)
#         self.alu('MUL', reg_a, reg_b)

#     def handle_HLT(self, a, b):
#         running = False
#         self.pc += 1

#     def handle_PUSH(self, a, b):
#         # * Decrements register at SP by one
#         val = self.register[a]
#         self.register[self.sp] -= 1
#         # * Copies the value at the given register to the address pointed to by SP
#         self.ram_write(val, self.register[self.sp])
#         # self.ram[self.register[self.sp]] = val
#         self.pc += 2

#     def handle_POP(self, a, b):
#         reg = a
#         val = self.ram_read(self.register[self.sp])
#         self.register[reg] = val
#         # * Incrememnt value at SP
#         self.register[self.sp] += 1
#         self.pc += 2


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 256
        self.register = [0] * 8
        self.sp = 7
        self.fl = 0

    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
            print('usage: file.py filename')
            sys.exit()

        filename = sys.argv[1]

        try:
            with open(filename) as f:
                for line in f:
                    # ignore comments
                    comment_split = line.split('#')
                    # remove whitespace
                    instruction = comment_split[0].strip()

                    if instruction == '':
                        continue
                    instruction = int(instruction, 2)
                    self.ram_write(instruction, address)
                    address += 1
        except FileNotFoundError:
            print('File not Found')
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        if op == 'MUL':
            self.register[reg_a] *= self.register[reg_b]
        # TODO -- add SUB functionality and use for CMP
        if op == 'CMP':
            if self.register[reg_a] - self.register[reg_b] > 0:
                # ! A is less than B -- use code '1'
                self.fl = 1
            if self.register[reg_b] - self.register[reg_a] > 0:
                # ! B is less than A -- use code '2'
                self.fl = 2
            elif self.register[reg_a] - self.register[reg_b] == 0:
                # ! A is equal to B -- use code '3'
                self.fl = 3

        if op == 'AND':
            self.register[reg_a] = self.register[reg_a] & self.register[reg_b]

        if op == 'OR':
            self.register[reg_a] = self.register[reg_a] | self.register[reg_b]

        if op == 'XOR':
            self.register[reg_a] = self.register[reg_a] ^ self.register[reg_b]

        if op == 'NOT':
            self.register[reg_a] = ~self.register[reg_a]

        if op == 'SHL':
            self.register[reg_a] = self.register[reg_a] << self.register[reg_b]

        if op == 'SHR':
            self.register[reg_a] = self.register[reg_a] >> self.register[reg_b]

        if op == 'MOD':
            if self.register[reg_b] == 0:
                print('Error: second register cannot be zero.')
            else:
                self.register[reg_a] = self.register[reg_a] % self.register[reg_b]

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    def ram_read(self, mar):
        return self.ram[mar]

    def interpret_command(self, opcode):
        commands = {
            0b10000010: 'LDI',
            0b01000111: 'PRN',
            0b00000001: 'HLT',
            0b10100000: 'ADD',
            0b10100010: 'MUL',
            0b01000101: 'PUSH',
            0b01000110: 'POP',
            0b01010000: 'CALL',
            0b00010001: 'RET',
            0b10100111: 'CMP',
            0b01010110: 'JNE',
            0b01010101: 'JEQ',
            0b01010100: 'JMP',
            0b10101000: 'AND',
        }
        return commands[opcode]

    def run(self):
        """Run the CPU."""
        command = ''
        running = True

        while running:
            command = self.ram_read(self.pc)
            # print('command', command)
            ir = self.interpret_command(command)
            # print('ir', ir)
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)
            if ir == 'LDI':
                self.register[operand_a] = operand_b
                self.pc += 3
            if ir == 'MUL':
                self.alu('MUL', operand_a, operand_b)
                self.pc += 3
            if ir == 'PRN':
                print(self.register[operand_a])
                self.pc += 2

            if ir == 'PUSH':
                # * Decrements register at SP by one
                val = self.register[operand_a]
                self.register[self.sp] -= 1
                # * Copies the value at the given register to the address pointed to by SP
                self.ram_write(val, self.register[self.sp])
                self.pc += 2

            if ir == 'POP':
                val = self.ram_read(self.register[self.sp])
                self.register[operand_a] = val
                # * Incrememnt value at SP
                self.register[self.sp] += 1
                self.pc += 2

            if ir == 'HLT':
                running = False
                self.pc += 1

            if ir == 'ADD':
                self.alu('ADD', operand_a, operand_b)
                self.pc += 3

            if ir == 'CALL':
                self.register[self.sp] -= 1
                self.ram[self.register[self.sp]] = self.pc + 2
                self.pc = self.register[operand_a]

            if ir == 'RET':
                val = self.ram[self.register[self.sp]]
                self.pc = val
                self.register[self.sp] += 1

            if ir == 'CMP':
                self.alu('CMP', operand_a, operand_b)
                self.pc += 3

            if ir == 'JMP':
                loc = self.register[operand_a]
                self.pc = loc

            if ir == 'JNE':
                if self.fl == 1 or self.fl == 2:
                    loc = self.register[operand_a]
                    self.pc = loc
                else:
                    self.pc += 2

            if ir == 'JEQ':
                if self.fl == 3:
                    loc = self.register[operand_a]
                    self.pc = loc
                else:
                    self.pc += 2

            if ir == 'AND':
                self.alu('AND', operand_a, operand_b)
                self.pc += 3

            if ir == 'OR':
                self.alu('OR', operand_a, operand_b)
                self.pc += 3

            if ir == 'XOR':
                self.alu('XOR', operand_a, operand_b)
                self.pc += 3

            if ir == 'NOT':
                self.alu('NOT', operand_a, operand_b)
                self.pc += 2

            if ir == 'SHL':
                self.alu('SHL', operand_a, operand_b)
                self.pc += 3

            if ir == 'SHR':
                self.alu('SHR', operand_a, operand_b)
                self.pc += 3

            if ir == 'MOD':
                self.alu('MOD', operand_a, operand_b)
                self.pc += 3
