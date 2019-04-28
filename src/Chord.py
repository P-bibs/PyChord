import functools
import Tables

class Chord:
    def __init__(self, root, intervals, bass):
        # PitchName object
        self.root = root
        # tuple of Interval object
        self.intervals = intervals
        # PitchName object
        self.bass = bass

        self.spelling = []

    # returns each characteristic of chord concatenated (ie: root + quality + size)
    def toString(self):
        return self.root + ":" + str(self.intervals) + "/" + self.bass

    # Gets spelling, or returns cached version if already computed
    def getSpelling(self):
        if self.spelling == []:
            notes = [self.root]

            for i in range(1, len(self.intervals)):
                notes.append(self.noteFromInterval(self.intervals[i]))

            self.spelling = notes

        return notes

    def getNoteArray(self):
        noteArray = [0 for c in range(12)]
        rootNumeral = Tables.notes["naturalToHalfStep"][self.root]
        noteArray[rootNumeral % 12] = 1

        for i in range(len(self.intervals)):
            halfStep = self.intervals[i][1]
            noteArray[(rootNumeral+halfStep) % 12] = 1

        return noteArray

    def getPseudoHash(self):
        noteArray = self.getNoteArray()
        pseudoHash = ''
        for i in range(0, 12, 3):
            seg = functools.reduce((lambda a,b : str(a)+str(b)), noteArray[i:i+3])
            pseudoHash += str(chr(int(seg, 2) + 97))
        
        return pseudoHash

    def noteFromInterval(self, interval):
        # -1 is added because an interval of a first corresponds to the root pitch
        rootNumeral = Tables.notes["naturalToStep"][self.root[0]]-1
        natural = Tables.notes["stepToNatural"][str(((rootNumeral + interval[0]) % 7))]

        naturalHalfSteps = Tables.notes["naturalToHalfStep"][natural]
        rootHalfSteps = Tables.notes["naturalToHalfStep"][self.root]

        # This is necessary for it all to work. Don't ask why
        if self.root=="Cb":
            naturalHalfSteps+=12

        if (naturalHalfSteps - rootHalfSteps)<0:
            halfStepOffset = interval[1]%12 - (naturalHalfSteps+12 - rootHalfSteps)
        else:
            halfStepOffset = interval[1]%12 - (naturalHalfSteps - rootHalfSteps)

        if halfStepOffset == 0:
            accidental = ""
        elif halfStepOffset > 0:
            accidental = "#" * halfStepOffset
        elif halfStepOffset < 0:
            accidental = "b" * (-1*halfStepOffset)

        return natural + accidental