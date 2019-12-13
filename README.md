# Boggle
A quick-and-dirty Boggle board solver.

I wrote this as something to do on a flight to Chigago, mostly because I
disagree with the choice of word list used by
[WEBoggle](http://weboggle.info/).

It's hacky but it solves most 4x4 Boggle boards in one second or less.  The
mean time per board over a 1000-run benchmark was 0.58 seconds per board.

The board traversal code is simple but isn't particularly performant.  However,
it is easy to drastically reduce the number of words that need to be searched.
Prior to search, the word list is pruned; words longer than 16 letters and
words containing letters absent from the board are removed from consideration.

As a result, the code is good enough to serve as an answer key.  Since
more than 1000 words per second can be searched, the code could also serve as
the basis for an interactive application similar to WEBoggle.

# Setup
This project requires Python 3.7 and `click`.

# Word list
We use the [Collins Scrabble Words (2015)](https://drive.google.com/file/d/0B9-WNydZzCHrdDVEc09CamJOZHc/view).
