"""CPU functionality."""

import sys
import os

""" 
#TODO LDI: Load Immediately, store values to register OR set register to values
loading puts into a particular defined register to a specific value defined instructions
#TODO PRN: Print, a pseudo=instruction (to print register numeric value )
Raw print file created by a "print to file" 
#TODO HLT: Halt, CPU and exits emulator
Assembly language instructions to stop if system enters an idle state
Does not continue until the next external interrput is fired
#TODO MUL Unsigned Multiply 
Multiplies 8-, 16-, or 32 format reg8/mem8, reg16/mem16, reg32/mem32
#TODO NOP No Operations
Commonly used for timing purposes, aligning memory, prevent hazards, create branch delay slot,
render existing instruction void
"""

class CPU:
    """Main CPU class."""
    def __init__(self):
    #TODO Implemented all CPU Constructor
        self.ram = [0] * 256
        self.reg = [0x00] * 8
        self.pc = 0x00
        self.sp = 0xf4
        self.ir = 0x00
        self.mar = 0x00
        self.mdr = 0x00
        self.fl = 0x00
        self.heap_height = 0
        self.running = True
        self.op_arr = {1: {0: {0b0000: 'ADD',
                               0b1000: 'AND',
                               0b0111: 'CMP',
                               0b0110: 'DEC',
                               0b0011: 'DEV',
                               0b0101: 'INC',
                               0b0100: 'MOD',
                               0b0010: 'MUL',

                               0b0001: 'SUB',
                               }},
                       0: {1: {0b0000: 'CALL',
                               0b0010: 'INT',
                               0b0011: 'IRET',
                               0b0101: 'JEQ',
                               0b1010: 'JGE',
                               0b0111: 'JGT',
                               0b1001: 'JLE',
                               0b1000: 'JLT',
                               0b0100: 'JMP',
                               0b0110: 'JNE',
                               0b0001: 'RET',
                               },
                           0: {0b0001: 'HLT',
                               0b0011: 'LD',
                               0b0010: 'LDI',
                               0b0000: 'NOP',
                               0b0110: 'POP',
                               0b1000: 'PRA',
                               0b0111: 'PRN',
                               0b0101: 'PUSH',
                               0b0100: 'ST',
                               }
                           }
                       }
        def exit(self):
            sys.exit()

    def load(self):
        args = sys.argv[1:]
        if args:
            file = os.path.join(args[0])
            with open(file, 'r') as f:
                for line in f:
                    line = line.split('#')[0].strip()
                    # print('l', line)
                    if line == '':
                        continue
                    self.ram[self.heap_height] = f'{int(line, 2):08b}'
                    self.heap_height += 1
        else:
            
            raise ValueError("Unsupported ALU operation")
    def other(self, op, *args):
        """Not ALU operations."""
        if len(args) > 1:
            arg_1, arg_2 = int(args[0], 2), int(args[1], 2)
        elif len(args):
            arg_1 = int(args[0], 2)

        if op == 'PRN':
            print(int(self.reg[arg_1], 2), end='\n')

        elif op == 'PRA':
            address = int(self.reg[arg_1], 2)
            letter = self.ram[address]
            print(chr(int(letter, 2)), end='')

        elif op == 'LDI':
            self.reg[arg_1] = args[1]

        elif op == 'HLT':
            self.exit()

        elif op == 'LD':
            self.reg[arg_1] = self.reg[arg_2]

        elif op == 'PUSH':
            self.sp -= 1
            # print(self.sp, self.heap_height)
            if self.sp <= self.heap_height:
                raise IndexError('Stack Overflow')
            self.ram[self.sp] = self.reg[arg_1]

        elif op == 'POP':
            self.reg[arg_1] = self.ram[self.sp]
            self.sp += 1
            
        else:
            raise ValueError(f'No such opperation exists {op}')

    def alu(self, op, *args):
        """ALU operations."""
        if len(args) > 1:
            arg_1, arg_2 = int(args[0], 2), int(args[1], 2)
        else:
            arg_1 = int(args[0], 2)
            
        if op == "ADD":
            added = (int(self.reg[arg_1], 2) + int(self.reg[arg_2], 2)) & 0xff
            self.reg[arg_1] = f'{added:08b}'
        elif op == "SUB":
            subbed = (int(self.reg[arg_1], 2) - int(self.reg[arg_2], 2)) * 0xff
            self.reg[arg_1] = f'{subbed:08b}'
    # TODO add MUL function
        elif op == 'MUL':
            mulled = (int(self.reg[arg_1], 2) * int(self.reg[arg_2], 2)) & 0xff
            self.reg[arg_1] = f'{mulled:08b}'
        else:
            raise ValueError(f"Unsupported ALU operation: {op}")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()
    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self, address, value):
        self.ram[address] = value
        
    def run(self):
        while True:
            self.ir = int(self.ram_read(self.pc), 2)
            _bytes = self.ir >> 6
            _alu = self.ir & 0b00100000
            alu = _alu >> 5
            _adv_pc = self.ir & 0b00010000
            adv_pc = _adv_pc >> 4
            instruction = self.ir & 0b00001111
            args = []

            for _ in range(_bytes):
                self.pc += 1
                args.append(self.ram_read(self.pc))

            if not adv_pc:
                self.pc += 1
            op = self.op_arr[alu][adv_pc][instruction]

            if alu:
                self.alu(op, *args)
            else:
                self.other(op, *args)


