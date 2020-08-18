"""CPU functionality."""

import sys

LDI = 0b10000010
HLT = 0b00000001
PRN = 0b01000111
MUL = 0b10100010
NOP = 0b00000000

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
    #TODO Implement CPU Constructor
        self.ram = [0] * 256
        self.register = [0] * 8
        self.pc = 0
        self.running = True

    def load(self):
        filename = sys.argv[1]

        with open(filename) as f:
            for address, line in enumerate(f):
                line = line.split('#')
                try:
                    v = int(line[0], 2)
                except ValueError:
                    continue
                self.ram_write(address, v)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
    # TODO add MUL function
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

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

#TODO Created instructional functions to replace hard-coding to use with callback 
    def LDI(self):
        register_num = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        self.register[register_num] = value
        self.pc += 3

    def HLT(self):
        self.running = False
    
    def PRN(self):
        register_num = self.ram_read(self.pc + 1)
        print(self.register[register_num])
        self.pc += 2
    
    def MUL(self):
        register_num1 = self.ram_read(self.pc + 1)
        register_num2 = self.ram_read(self.pc + 2)
        self.alu("MUL", register_num1, register_num2)
        self.pc += 3

    def NOP(self):
        self.pc += 1

    def cb_func(self, n):
        branch_table = {
            NOP : self.NOP,
            HLT : self.HLT,
            PRN : self.PRN,
            LDI : self.LDI,
            MUL : self.MUL
        }

        f = branch_table[n]
        if branch_table.get(n) is not None:
            f()
        else:
            print(f'Unknown instruction {n} at address {self.pc}')
            sys.exit(1)

#TODO Replaced hard-coded functions with callback functions
    def run(self):
        while self.running:
            reg_instructor = self.ram_read(self.pc)
            self.cb_func(reg_instructor)
            

    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self, address, value):
        self.ram[address] = value