#! /usr/bin/env python3

import random
import sys

def main():
	arg1 = sys.argv[1]
	print(arg1)
	#writing to stderr
	#print("fatal error", file=sys.stderr)
	#sys.stderr.write("fatal error\n")

if __name__ == "__main__":
	main()
