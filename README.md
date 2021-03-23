# Using Q-learning algorithm for train rescheduling

[![](./img/logo.png)](https://)

Authors:
 - Anna Christina Kolandjian
 - Clarisse Pouillery
 
# 🎯 Goal
This program uses the Q-learning approach for train rescheduling. 
At the end, it prints the cumulated rewards and the obtained Q-table.

# 📝 Description 
It takes the two datetimes passed by the user and runs the Q-learning
algorithm during the given time window.


The output is in the format:

```bash
bla bla bla
```

# 💻 Software Development
### File Hierarchy
```
Qlearning
├── run.py
├── qlearning.py
├── initialize.py
├── visualization.txt
├── usefulData
│ ├── lineJ_windowHours.csv
│ ├── WT_from_PSL.csv
│ └── trains_J_from_PSL.json
├── OD
│ └── J_normalized.csv
│ 
└── README.md
```
### Development

- run.py: 
   - Takes the input datetimes, if they were given by the user in the command, else asks for two proper datetimes.
   - Calls the primary method of initialize.py: getResult() 
- qlearning.py:
   - Once its primary method getResult() is called, it validates the datetimes (if they're not valid, it asks for new ones).
   - Calls the initialize.py method set_variables() to initialize all variables and parameters.
   - It runs the algorithm.
- initialize.py:
   - It takes the two datetimes and creates a file windowHours containing all information about trains, stations, time slots.
   - It produces a reward dictionary with stations as keys and rewards as values.

# ⚠️ Note to Users


# ❓ How To Use

* 🏃 Execute run.py
```bash
$ python3 run.py <datetime 1> <datetime 2>
```
In our case:
```bash
$ python3 run.py 2020-02-13T10:00:00.000Z 2020-02-13T11:30:00.000Z
```
* 🏁 Expected output

![](./img/expected-output.png)]

# 📙 About SNCF
- 
- 📞 Contact:


# 📃 License

Licensed under SNCF ©2021. See the license for the details.
