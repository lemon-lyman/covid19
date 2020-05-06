from classes import Graph
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        Graph(sys.argv[1])
    else:
        Graph()