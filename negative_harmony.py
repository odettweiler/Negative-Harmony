import mingus.core.notes as notes
import mingus.core.intervals as intervals
import mingus.core.chords as chords
import mingus.core.notes as notes
import mingus.core.mt_exceptions as exceptions
import PySimpleGUI as sg

# mingus is used for theory applications
# PySimpleGUI is used for visuals

# goal: to automate the use of negative harmony using Object Oriented Programming and a simple gui
# this is done by creating a reflection matrix based on two notes, a fifth apart
# then this is expanded through the matrix, which is based on the circle of fifths
# this creates the effect of flipping a note over the axis note between the two notes given
# flipping across the matrix. This can be used with single notes as well as chords, 
# and chord shorthand can be used as well.

'''
example reflection matrix for F-C:
[[F,C],
[Bb,G],
[Eb,D],
[Ab,A],
[C#,E],
[F#,B]]
'''

# harmonizer object to get 
class NegativeHarmonizer:
    # initialize the harmonizer
    def __init__(self, note1, note2):
        self.axis_note1 = note1 # first note
        self.axis_note2 = note2 # second note, a fifth above (this is checked prior to initialization)
        # generate matrix based on these two notes
        self.generate_reflection_matrix(self.axis_note1, self.axis_note2)

    def generate_reflection_matrix(self, note1, note2):
        # gen blank reflection matrix
        matrix = [[ None for x in range(2)] for y in range(6)]
        # input first axis notes into matrix
        matrix[0][0] = note1; matrix[0][1] = note2

        # traverse matrix downwards
        row = 0
        while row < 5: # input perfect fifth intervals
            matrix[row+1][1] = intervals.from_shorthand(matrix[row][1], "5")
            row += 1

        matrix[5][0] = intervals.from_shorthand(matrix[5][1], "5") # init for backward traversing
        row = 5 # traverse up the matrix
        while row > 1:
            matrix[row-1][0] = intervals.from_shorthand(matrix[row][0], "5")
            row -= 1

        # clean up matrix for it to look nice
        for x in range(6):
            for y in range(2): # check each note and sub notes for standardization
                if matrix[x][y] == "Fb":
                    matrix[x][y] = "E"
                if matrix[x][y] == "E#":
                    matrix[x][y] = "F"
                if matrix[x][y] == "B#":
                    matrix[x][y] = "C"
                if matrix[x][y] == "Cb":
                    matrix[x][y] = "B"
                if matrix[x][y] == "A#":
                    matrix[x][y] = "Bb"
                if matrix[x][y] == "D#":
                    matrix[x][y] = "Eb"
                if matrix[x][y] == "G#":
                    matrix[x][y] = "Ab"

        self.matrix = matrix # reassign matrix variable
        
    def get_note_pos(self, note):
        # traverse until you find it, nested for loops
        for x in range(6):
            for y in range(2): # check each note
                # check if it's the same using note_to_int
                if notes.note_to_int(self.matrix[x][y]) == notes.note_to_int(note):
                    return x, y # if it's the same, return position in a tuple

    def invert_note(self, note):
        # look up note position
        note_pos = self.get_note_pos(note)
        # if it's in the left side, get the right side, vice versa
        if (note_pos[1] == 0): # left side
            return self.matrix[note_pos[0]][1]
        if (note_pos[1] == 1): # right side
            return self.matrix[note_pos[0]][0]

    def invert_chord(self, chord):
        new_chord = [] # new chord array
        for note in chord: # flip each note
            new_chord.append(self.invert_note(note)) # add to array

        return new_chord # return array
    
def swap(arr, pos1, pos2): # swap function for array because i couldn't find one natively
    temp = arr[pos1] # temporary variable with 1's value
    arr[pos1] = arr[pos2] # put 2 in 1's place
    arr[pos2] = temp # put temporary value in 2's place
    return arr # give back array

def get_note_combos(notes):
    note_matrix = [[None for x in range(len(notes))] for y in range(1)] # generate combination matrix
    note_matrix[0] = notes # first combo is given
    count = 0 # keep track of number
    for x in range(len(notes)): # for each note
        for y in range(len(notes)): # for each other note
            if y != x: # if it's a different note
                note_matrix.append(swap(note_matrix[count-1].copy(), x, y)) # swap these two notes, add to array
                count += 1 # add to count of combinations

    return note_matrix # return combinations

def get_chord_names(notes, num=5):
    # swap around notes, appending all names
    combos = get_note_combos(notes)

    names = [] # name matrix
    for combo in combos: # get each note order combination
        possible_names = chords.determine(combo, True) # might return nothing, or names
        if possible_names: # if there are names
            for name in chords.determine(combo, True): # take each name
                if name not in names: # if it's not already in there
                    names.append(name) # add it to name array

    return sorted(names, key=len)[:num] # order by name length and return, might be empty array

def simplify_chord(notes):
    # return notes in a different order based on simplest chord name
    names = get_chord_names(notes)
    if not names: # zero possible names
        return notes
    # use above function and take first one
    name = names[0]
    noteCount = 0
    for note in chords.from_shorthand(name):
        # return if they have the same notes
        if note in notes:
            noteCount += 1

    ret_notes = notes # start with input notes
    if noteCount == len(notes): # if the chord shorthand returns the same number of notes
        ret_notes = chords.from_shorthand(name) # return if it works
    else:
        print("chord could not be simplified:", notes)

    ret = ""
    for note in ret_notes:
        ret = ret + note + " " # add each note in the array

    return ret

shorthand_guide = """Triads: 'm', 'M' or '', 'dim'.
Sevenths: 'm7', 'M7', '7', 'm7b5', 'dim7', 'm/M7' or 'mM7'
Augmented chords: 'aug' or '+', '7#5' or 'M7+5', 'M7+', 'm7+', '7+'
Suspended chords: 'sus4', 'sus2', 'sus47', 'sus', '11', 'sus4b9' or 'susb9'
Sixths: '6', 'm6', 'M6', '6/7' or '67', 6/9 or 69
Ninths: '9', 'M9', 'm9', '7b9', '7#9'
Elevenths: '11', '7#11', 'm11'
Thirteenths: '13', 'M13', 'm13'
Altered chords: '7b5', '7b9', '7#9', '67' or '6/7'
Special: '5', 'NC', 'hendrix'"""

harmonizer = NegativeHarmonizer("C", "G")
print("Negative harmonizer initialized!")
print(harmonizer.matrix)

# post-application output to be printed
print_output = ''

# GUI Time :)
sg.theme('DarkGreen3')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.T('What are you axis notes?'), sg.I(key='-NOTE1-', size=5), sg.I(key='-NOTE2-', size=5), sg.B('Invert')],
            [sg.T("                ")],
            [sg.T("Notes: "), sg.I(key='-NOTES-', size=20), sg.T("---------------------------"), sg.Output(size=(20,5), key='-NOTESOUT-')],
            [sg.T("                ")],
            [sg.T("Chord: "), sg.I(key='-CHORD-', size=20), sg.CB('Use shorthand', key='-SHORTHAND-'), sg.Output(size=(20,5), key='-CHORDOUT-')]]

# Create the Window
window = sg.Window('Negative Harmony Automation', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
        break
    elif event == 'Invert':
        # set up with new axis notes if necessary
        if values["-NOTE1-"] != '' and values["-NOTE2-"] != '': # both are filled in
            if notes.is_valid_note(values["-NOTE1-"]) and notes.is_valid_note(values["-NOTE2-"]): # valid notes
                if intervals.measure(values["-NOTE1-"], values["-NOTE2-"]) == 7: # perfect fifth
                    harmonizer = NegativeHarmonizer(values["-NOTE1-"], values["-NOTE2-"]) # reinitialize harmonizer
                else: # otherwise popup with error
                    sg.popup('Notes are not a fifth apart', values["-NOTE1-"], values["-NOTE2-"])
                    continue # cancel inversion
            else: # invalid notes
                sg.popup("Note is not valid!", values["-NOTE1-"], values["-NOTE2-"])
                continue # cancel inversion

        noteIn = values["-NOTES-"] # get input
        noteOut = "" # init note output
        chordIn = values["-CHORD-"] # get input
        chordOut = "" # init chord output

        # evaluate noteIn
        if noteIn.__contains__(" "): # multiple notes
            split_notes = noteIn.split(" ") # split by space
            for note in split_notes: 
                if notes.is_valid_note(note): # if a note is valid
                    noteOut = noteOut + harmonizer.invert_note(note) + " " # flip note and add to output
                else: 
                    sg.popup('Invalid note!', note) # if there's a wrong note, show onscreen
        elif noteIn != '':
            if notes.is_valid_note(noteIn): # valid note
                noteOut = harmonizer.invert_note(noteIn) # invert note and add to output
            else:
                sg.popup('Invalid note!', noteIn) # wrong note, show onscreen
        else:
            noteOut = '' # no notes, leave output blank

        # chord management
        if chordIn != '':
            if values['-SHORTHAND-']: # use shorthand
                chord_notes = ''
                try: 
                    chord_notes = chords.from_shorthand(chordIn) # if shorthand works, import notes
                except exceptions.FormatError or exceptions.NoteFormatError: # exception for error
                    sg.popup("This is not a valid chord! Valid shorthand is shown below:", 
                             shorthand_guide) # show shorthand guide if it's wrong
                    chordOut = '' # cancel output
                if chord_notes != '' and chord_notes != []: # if there's a chord
                    new_chord = harmonizer.invert_chord(chord_notes) # invert it
                    chord_names = get_chord_names(new_chord) # get the possible names
                    chord_notes_reordered = simplify_chord(new_chord) # simplify the chord
                    # then print out the reordered notes, the more concise name, and alternate names
                    if len(chord_names) > 1: # two or more names, show shortest and others
                        chordOut = chord_notes_reordered + " | " + chord_names[0] + "\n" + "Alternate chord names: " + "\n" + chord_names[1:].__str__()
                    elif len(chord_names) == 1: # only one, show main one
                        chordOut = chord_notes_reordered + " | " + chord_names[0]
                    elif len(chord_names) == 0: # no naming, show only the notes
                        chordOut = chord_notes_reordered
            else:
                if chordIn.__contains__(" "): # multiple notes
                    split_chord = chordIn.split(" ") # split by space
                    chord_notes = []
                    wrong_notes = []
                    for note in split_chord:
                        if notes.is_valid_note(note): # if there's a correct note
                            chord_notes.append(note) # put it in the chord notes
                        else: # otherwise it's put in wrong_notes
                            wrong_notes.append(note)
                    if len(wrong_notes) > 0: # if there are any wrong notes
                        sg.popup('Invalid note!', wrong_notes) # show onscreen
                        chordOut = '' # and cancel output
                    else: # if there are no wrong notes, continue
                        new_chord = harmonizer.invert_chord(chord_notes) # invert chord
                        chord_names = get_chord_names(new_chord) # get new names
                        chord_notes_reordered = simplify_chord(new_chord) # get reordered notes
                        # print out the notes, name, and alternate names
                        chordOut = chordOut = chord_notes_reordered + " | " + chord_names[0] + "\n" + "Alternate chord names: " + "\n" + chord_names[1:].__str__()
                else: # only one note, use notes part instead
                    sg.popup('Please input multiple notes. Otherwise put this in notes.')
                    chordOut = '' # cancel output
        else:
            chordOut = '' # cancel output if there is no text

        # update window with output
        window["-NOTESOUT-"].update(noteOut)
        window["-CHORDOUT-"].update(chordOut)

window.close()
print(print_output)
print("Negative harmonizer shut down!")