# University Class Scheduling Problem (USCP)

This repo is dedicated to Roy Lim z5310629's work for COMP4121 Advanced Algorithms.

University Class Scheduling Problem (USCP) is an important but difficult problem for
universities due to the recent explosion in enrolments and courses. Currently, timetable
creation is done manually at UNSW due to the number of both hard and soft constraints,
tho UNSW has developed algorithms to assist the process. In addition, due to different
universities having different circumstances, there is no commercial solution suitable for the
problem yet. This project briefly analyzes and implements three different algorithms and discusses how they can
be augmented to solve the problem.: Binary Integer Programming, Genetic Algorithms
and Ant Colony Algorithm. After implementing the algorithms, we determined that Ant
Colony Optimization was the most suitable candidate for a large-scale implementation
due to its speed, flexibility, and portability. Further optimization is required before the
algorithm is ready to be used.

Implementation of algorithms can be found in:
```shell
linearScheduler.py
geneticSchedule.py
antColonyScheduler.py
```

You can run them using their corrosponding `main.py` files.


