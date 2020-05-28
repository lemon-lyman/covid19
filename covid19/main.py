from classes import Graph
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        output = Graph(sys.argv[1])
    else:
        output = Graph()