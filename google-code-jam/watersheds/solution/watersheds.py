#!/usr/bin/env python

#    Desc: Answer to Google Code Jam 2009 Qualification Round: "Watersheds" Problem
#          https://code.google.com/codejam/contest/90101/dashboard#s=p1
# Created: January 2013
#  Status: Successful with Google Code Jam sample input
#  Author: Vahid Pazirandeh (vpaziran@gmail.com)

import sys
from functools import total_ordering


@total_ordering
class Cell:
    def __init__(self, altitude):
        self.altitude = altitude
        self.regionLabel = None
        # Neighboring cells seems to be more related to the Map class.
        # Should these attributes be moved there? Or maybe Cell should
        # be a nested class of Map (aggregate type)?
        self.neighborNorth = None
        self.neighborWest = None
        self.neighborEast = None
        self.neighborSouth = None

    def __eq__(self, other):
        return self.altitude == other.altitude

    def __lt__(self, other):
        return self.altitude < other.altitude

    def __str__(self):
        return self.regionLabel or '*'


class Map:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.rowIndex = 0
        self.colIndex = 0
        self.rows = []
        labels = list('abcdefghijklmnopqrstuvwxyz')
        labels.reverse()
        self.regionLabels = labels

    def addRow(self, row):
        self.rows.append(map(Cell, row))
        lastRowIndex = len(self.rows) - 1

        # Create double link between neighboring cells.
        for i, cell in enumerate(self.rows[lastRowIndex]):
            northCell = self._getNorthCell(lastRowIndex, i)
            if northCell:
                cell.neighborNorth = northCell
                northCell.neighborSouth = cell

            westCell = self._getWestCell(lastRowIndex, i)
            if westCell:
                cell.neighborWest = westCell
                westCell.neighborEast = cell

    def _getNorthCell(self, rowIndex, colIndex):
        if self._validPos(rowIndex-1, colIndex):
            return self.rows[rowIndex-1][colIndex]
        else:
            return None

    def _getWestCell(self, rowIndex, colIndex):
        if self._validPos(rowIndex, colIndex-1):
            return self.rows[rowIndex][colIndex-1]
        else:
            return None

    def _validPos(self, rowIndex, colIndex):
        return rowIndex >= 0 and rowIndex < len(self.rows) \
            and colIndex >= 0 and colIndex < len(self.rows[0])

    def _getLowestNeighbor(self, cell):
        # Neighbors here are listed in tie-breaker precedence order.
        neighboringCells = [cell.neighborNorth, cell.neighborWest, cell.neighborEast, cell.neighborSouth]
        neighboringCells = filter(lambda x: x != None, neighboringCells)
        lowestCell = min(neighboringCells)
        # It's possible for more than one cell to have the same altitude.
        # Tie breaker algorithm follows:
        for neighboringCell in neighboringCells:
            # Object value comparison, not necessarily the same object in memory.
            # TODO: Too complex? Make code simpler.
            if neighboringCell == lowestCell:
                return neighboringCell

    def labelRegions(self):
        for row in self.rows:
            for cell in row:
                lowestNeighbor = self._getLowestNeighbor(cell)
                if cell > lowestNeighbor:
                    label = lowestNeighbor.regionLabel or cell.regionLabel or self.regionLabels.pop()

                    # TODO: What if lowestNeighbor.regionLabel != cell.regionLabel != None ?
                    # Use Cell.upstreamCell and downstreamCell in order to solve this.

                    cell.regionLabel = label
                    lowestNeighbor.regionLabel = label
                else:
                    if not cell.regionLabel:
                        cell.regionLabel = self.regionLabels.pop()

    # An absolutely unnecessary iterator solely for the purpose of having some practice
    # implementing a class with an iterator. See self.__str__().
    def __iter__(self):
        for row in self.rows:
            for cell in row:
                yield cell

    def __str__(self):
        columnIndex = 0
        columnLen = len(self.rows[0])
        result = []
        for cell in self:
            if columnIndex == columnLen:
                result.append('\n')
                columnIndex = 0
            result.append('{} '.format(cell))
            columnIndex += 1
        return ''.join(result)


class ProblemInput:
    def __init__(self, inputFilePath):
        self.mapSpecs = []

        with open(inputFilePath) as inStream:
            # TODO: Is there a better way to read in an int?
            numMapSpecs = int(inStream.readline().rstrip())

            for i in range(numMapSpecs):
                # Tuple of (height, width).
                dimensions = inStream.readline().rstrip().split()

                # TODO: If a list does not need moficiation, is it best practice
                # to always convert it into a tuple? And is this the best way?

                # TODO: For small data items like dimensions, is it good to use
                # this tuple, or is a dictionary better, or maybe a class with data
                # attributes?

                dimensions = tuple(map(int, dimensions))
                height = dimensions[0]

                rows = []
                for j in range(dimensions[0]):
                    row = inStream.readline().rstrip().split()
                    rows.append(tuple(map(int, row)))

                self.mapSpecs.append({'dimensions': dimensions,
                                      'altitudeRows': rows})


class ProblemOutput:
    def __init__(self, problemInput, resultOutStream):
        self.problemInput = problemInput
        self.outStream = resultOutStream

    def run(self):
        for i, mapSpec in enumerate(self.problemInput.mapSpecs):
            height, width = mapSpec['dimensions']
            resultMap = Map(height, width)

            for row in mapSpec['altitudeRows']:
                resultMap.addRow(row)

            resultMap.labelRegions()
            self.outStream.write('Case #{}:\n'.format(i+1))
            self.outStream.write('{}\n'.format(resultMap))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: {} <pathToProblemInputFile>'.format(sys.argv[0])
        sys.exit(1)

    input = ProblemInput(sys.argv[1])
    output = ProblemOutput(input, sys.stdout)
    output.run()

# EOF
