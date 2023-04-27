# Negative-Harmony
This python application automates the use of negative harmony for notes and chords. This is augmented by a simple GUI through PySimpleGUI, and uses mingus for programming using theory concepts.

# Use of application
The app creates negative harmony by flipping over an axis, which is done by creating a reflection matrix around two notes, one perfect fifth apart. 
To begin, input your two axis notes at the top of the screen. By default, these are C and G, meaning the notes will be reflected over the axis of E half flat.
If these inputs are left blank, they use the last two notes inputted, which may not be shown.

To invert single notes, input them into the notes input section. 
These will be inverted using the reflection matrix and shown in the notes output section on the right side of the screen.

To invert chords, you have two options:
 - Input the notes individually, as you would in the notes section
 - Input chord shorthand, e.g.: "Gmaj7"
 These will be inverted through the reflection matrix and output, showing reordered notes, the shortest shorthand name, and alternate names for the chord.

To invert chords and notes, click the "Invert" button at the top right of the screen. This will output the negative harmony on the right side of the screen.
