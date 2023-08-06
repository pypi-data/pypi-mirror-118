import argparse
from math import pi,sqrt
parser = argparse.ArgumentParser(description="Process cmd command")
parser.add_argument("--L",'-l',dest = "inductance",type = float,help="Inductance of inductor",default=0)
parser.add_argument("--C",'-c',dest = "capacitance",type = float,help="Capacitance of capacitor",default=0)
parser.add_argument("--F",'-f',dest = "frequency",type = float,help="frequency",default=0)

# parser.add_mutually_exclusive_group('')
args = parser.parse_args()

def convert_unit(value):
    if(value>1e6):
        return "%1.2f"%(value/1e6)+"M"
    if(value>1e3):
        return "%1.2f"%(value/1e3)+"k"
    if(value>1):
        return "%1.2f"%value
    if(value>1e-3):
        return "%1.2f"%(value*1e3)+"m"
    if(value>1e-6):
        return "%1.2f"%(value*1e6)+"u"
    if(value>1e-9):
        return "%1.2f"%(value*1e9)+"n"
    if(value>1e-12):
        return "%1.2f"%(value*1e12)+"p"

def main():
    if(args.frequency == 0):
        freq = 1/(2*pi*sqrt(args.inductance*args.capacitance))
        print("Frequency is %s"%convert_unit(freq)+"Hz")
    else:
        if(args.capacitance):
            ind = 1/(2*pi*args.frequency)**2/args.capacitance
            print("Inductor is %s"%convert_unit(ind)+"H")
        else:
            cap = 1/(2*pi*args.frequency)**2/args.inductance
            print("Capacitor is %s"%convert_unit(cap)+"F")

if __name__ == '__main__':
    main()