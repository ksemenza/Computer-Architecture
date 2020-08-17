"""CPU functionality."""

import sys

""" 
#TODO LDI: Load Immediately, store values to register OR set register to values
 loading puts into a particular defined register to a specific value defined instructions
 
#TODO PRN: Print, a pseudo=instruction (to print register numeric value )
Raw print file created by a "print to file" 


#TODO HLT: Halt, CPU and exits emulator
Assembly language instructions to stop if system enters an idle state
Does not continue until the next external interrput is fired

"""

class CPU:
    """Main CPU class."""
#TODO Constants
    LDI = 0b10000010
    HLT = 0b00000001
    PRN = 0b01000111
    
    
    def __init__(self):
        """Construct a new CPU."""
#TODO Implement CPU Constructor
        self.ram = [0] * 256
        self.register = [0] * 8
        self.pc = 0
#TODO Running state
        self.running = True
        pass

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
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

#TODO initate running 
    def run(self):
        while self.running:
            reg_instructor = self.ram_read(self.pc)
            if reg_instructor == self.LDI:
                register_num = self.ram_read(self.pc + 1)
                value = self.ram_read(self.pc + 2)
                self.ram_write(register_num, value)
                self.pc += 3
            elif reg_instructor == self.HLT:
                self.running = False
            elif reg_instructor == self.PRN:
                register_num = self.ram[self.pc + 1]
                print(self.ram[register_num])
                self.pc += 2
            else:
                print(f'Error: Instruction {reg_instructor} at address {self.pc}')
                sys.exit(1)

#TODO Add read/write RAM functions
    #2-1 create ram_read 
    def ram_read(self, address):
        return self.ram[address]
    
    #2-2 create ram_write
    def ram_write(self, address, value):
        self.ram[address] = value
