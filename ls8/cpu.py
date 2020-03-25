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


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 256
        self.register = [0] * 8
        self.sp = 7

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
        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        if op == 'MUL':
            self.register[reg_a] *= self.register[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

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
        # opcode = int(opcode)
        # print(f'interpreter opcode: {opcode}')
        commands = {
            0b10000010: 'LDI',
            0b01000111: 'PRN',
            0b00000001: 'HLT',
            0b10100010: 'MUL',
            0b01000101: 'PUSH',
            0b01000110: 'POP'
        }
        # print('matching command = ', commands[opcode], type(commands[opcode]))
        return commands[opcode]

    def run(self):
        """Run the CPU."""
        command = ''
        running = True

        while running:
            command = self.ram_read(self.pc)
            ir = self.interpret_command(command)
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)
            # print(ir)
            # print('ram', self.ram)
            # print('register', self.register)
            if ir == 'LDI':
                self.register[operand_a] = operand_b
                self.pc += 3
            if ir == 'MUL':
                self.alu(ir, operand_a, operand_b)
                self.pc += 3
            if ir == 'PRN':
                print(self.register[operand_a])
                self.pc += 2

            if ir == 'PUSH':
                print('current operand_a', operand_a)
                # * Decrements register at SP by one
                val = self.register[operand_a]
                self.register[self.sp] -= 1
                # * Copies the value at the given register to the address pointed to by SP
                self.ram_write(self.register[self.sp], val)
                self.pc += 2

            if ir == 'POP':
                print('current operand_a', operand_a)
                reg = operand_a
                val = self.ram_read(self.register[self.sp])
                self.register[reg] = val
                # * Incrememnt value at SP
                self.register[self.sp] += 1
                self.pc += 2

            if ir == 'HLT':
                running = False
                self.pc += 1
            # else:
            #     print(f'ir {command} not recognized.')
            #     sys.exit()
