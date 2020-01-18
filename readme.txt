Team name: Daisy
Team members: Jasper Chapman-Black, Celine O'Neil, Sean Purcell
Project title: OEC 2020 Programming

All code is located in the top-level directory as *.py files.

To run the code, first install the one dependency, numpy.  This can be done via:
$ pip3 install -r requirements.txt

Then the code can be run as
$ python3 main.py <in.csv> <out.csv> [<cost weighting> <co2 weighting> <green weighting>]

The weightings are optional, and default to -1, -2, 0
(a negative number means the solver will attempt to minimize that value,
so we assign negative weight to cost and co2, and positive weight to green
production).

Our outputs for each of the 4 provided inputs are in output/.
