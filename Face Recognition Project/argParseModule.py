import argparse
import sys

def calc(args):
    if args.o == "add":
        return args.x + args.y
    elif args.o == "sub":
        return args.x- args.y
    elif args.o == "mul":
        return args.x*args.y
    elif args.o == "div":
        return args.x/args.y
    else:
        return "Invalid 😤."

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # creating an object of the class ArgumentParser()
    # this creats an python objects of the command-line arguments provided by the user
    parser.add_argument("--x",type=float,default=1.0,
                        help="Enter first number. This is used for calculation purposes.")
    parser.add_argument("--y",type=float,default=3.0,
                        help="Enter second number. This is used for calculation purposes.")
    parser.add_argument("--o",type=str,default="add",
                        help="This is utility for calculation.")
    
    args = parser.parse_args()
    sys.stdout.write(str(calc(args)))
