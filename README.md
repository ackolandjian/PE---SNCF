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
   - Takes the input file path, if it's given by the user in the command, else asks for an input file path.
   - Calls the primary method of wordcount.py: get.result() 
- wordcount.py:
   - Once its primary method get.result() is called, it validates the file path (if it's not valid, it asks for a new one). 
   - It splits the whole content of the text file by empty spaces and return it as a list of strings.
   - Calls the processtext.py method get.dict() to get the dictionary.
- processtext.py:
   - It takes the content of the file (list of strings) passed and produces a dictionary containing words as keys and individual word counts as values.
   - The dictionary is returned to the caller (wordcount.py).

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
