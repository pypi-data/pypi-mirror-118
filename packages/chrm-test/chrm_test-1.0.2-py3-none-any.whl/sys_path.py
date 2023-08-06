import sys
import pprint

pp = pprint.PrettyPrinter(indent=4)

if __name__ == "__main__":
  pp.pprint(sys.path)