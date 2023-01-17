# Project-Minor-Computational-Science


Profiling:
* pip install gprof2dot
* python -m cProfile -o data/profile.stats sim/main.py run
* gprof2dot data/profile.stats -f pstats > data/profile.dot
* dot -Tpng data/profile.dot -o data/profile.png
* open data/profile.png