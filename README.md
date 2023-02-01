# Project-Minor-Computational-Science
Developers: Jenna de Vries, Kato Schmidt, Derk Niessink

## User manual

We developed a simulation for modeling satellites and space debris. In this
simulation we use satellite and debris data in low-Earth orbit (LEO). The data
consist of more than 11000 objects, that is why for performance reasons, we
divided the data in groups. The groups are determined by the semi-major axes of
the objects, because objects that do not have a similar semi-major axis will
never collide.

### Running the simulation

* Navigate to `sim` directory -> `cd sim`
* Create a virtual environment -> `python3 -m venv venv`
* Download the required packages -> `pip install -r requirements.txt`
* Run the sim with a desired group number -> `python main.py [Group number] [view]`

An animation can be shown in the browser when adding the second argument "view".

So for example running group 5 with the the animation -> `python main.py 5 view`

And without the animation                             -> `python main.py 5`

### After the simulation

* Data will be saved in `sim_data` in the corresponding group number folder.
* A ZeroDivisionError will be printed in the terminal. There is nothing to do
about this and is caused by the fact that vpython (the animation library) has not
updated since the new version release of Python.

### For developers

Profiling:
* pip install gprof2dot
* python -m cProfile -o data/profile.stats sim/main.py
* gprof2dot data/profile.stats -f pstats > data/profile.dot
* dot -Tpng data/profile.dot -o data/profile.png
* open data/profile.png