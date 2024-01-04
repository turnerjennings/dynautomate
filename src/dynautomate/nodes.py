import numpy as np
from transformation import *

# object to handle nodes
class Nodes:
    def __init__(self, input_string: str, input_range: list[int], format: str):
        # define basic inputs
        self.name = "NODE"
        self.format = format
        self.string = input_string
        self.range = input_range

        # split lines and eject title line
        lines = input_string.split("\n")
        lines.pop(0)
        if lines[0][0:1] == "$":
            lines.pop(0)
        self.numnodes = len(lines)
        self.nodes = np.empty((len(lines), 6))

        # split nodal values depending on format
        for idx, string in enumerate(lines):
            match self.format:
                case "fixed":
                    line_values = string.split()
                    self.nodes[idx, :] = line_values

                case "long":
                    line_values = string.split()
                    self.nodes[idx, :] = line_values

                case "short":
                    line_values = string.split(",")
                    self.nodes[idx, :] = line_values

    # method to transform a set of nodes using a transformation operator
    def transform(self, node_set: list[int], operator: Transformation):
        tmatrix = operator.matrix

        for index in node_set:
            # extract nodal coordinates and reformat
            coordinates = self.nodes[index, 1:4]
            coordinates = np.hstack((coordinates, np.array([1])))
            coordinates = coordinates.reshape(-1, 1)

            # apply transformations
            new_coordinates = tmatrix @ coordinates
            print(f"New vector: {new_coordinates}")
            self.nodes[index, 1:4] = new_coordinates[0:3].transpose()
        self.update_string()

    # method to update the nodes string
    def update_string(self):
        lines = ["*NODE"]
        match self.format:
            case "fixed":
                for i in range(self.numnodes):
                    line_values = self.nodes[i, 0:]
                    line_string = (
                        f"{int(line_values[0]):8}".rjust(8)
                        + f"{line_values[1]:11G}".rjust(16)
                        + f"{line_values[2]:11G}".rjust(16)
                        + f"{line_values[3]:11G}".rjust(16)
                        + f"{line_values[4]:8G}".rjust(8)
                        + f"{line_values[5]:8G}".rjust(8)
                    )
                    lines.append(line_string)

            case "long":
                for i in range(self.numnodes):
                    line_values = self.nodes[i, 0:]
                    line_string = (
                        f"{int(line_values[0]):20}".rjust(20)
                        + f"{line_values[1]:15G}".rjust(20)
                        + f"{line_values[2]:15G}".rjust(20)
                        + f"{line_values[3]:15G}".rjust(20)
                        + f"{line_values[4]:15G}".rjust(20)
                        + f"{line_values[5]:15G}"
                    )
                    lines.append(line_string)

            case "short":
                for i in range(self.numnodes):
                    line_values = self.nodes[i, 0:]
                    line_string = (
                        f"{int(line_values[0])}"
                        + ","
                        + f"{line_values[1]}"
                        + ","
                        + f"{line_values[2]}"
                        + ","
                        + f"{line_values[3]}"
                        + ","
                        + f"{line_values[4]}"
                        + ","
                        + f"{line_values[5]}"
                        + ","
                    )
                    lines.append(line_string)

        self.string = "\n".join(lines)