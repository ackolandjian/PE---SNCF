# Using Machine learning algorithms and heuristics for train rescheduling

Authors:
 - Anna Christiane Kolandjian
 - Clarisse Pouillery
 - Peter Matta
 - Jean-Philippe Thai
 
# 🎯 Goal
Transilien is a railway system that is a major operator of Paris suburban trains. However, some operational decisions like skipping a train stop may impact the quality of service for passengers.
In order to optimize such decisions, we took two different approaches to propose a single algorithm for automatic train rescheduling.

# 📝 Description 
Based on the Transilien line J from the Parisian railway system, this report proposes two approaches to a train rescheduling problem in case of small disturbances. The possible decisions are the following: one or more stations of the line can be removed and the trains can be rescheduled one to a few minutes later than the original transport plan. A method using two heuristics is first presented. The objectives are to minimize recovery time and passengers' dissatisfaction. A reinforcement learning method is also proposed to assist the decision support tool and the operators. Simulations were performed on real data of the line J, in a given time window, to show the impact of rescheduling decisions. The comparison between these two methods and with other perspectives are also discussed.

# 💻 Software Development
### File Hierarchy
```
PE-SNCF-2021
├── Preprocessing
├── Heuristics
├── Qlearning
├── ressources
│ 
└── README.md
```
### Development

## Preprocessing
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
   - It initializes the Q-table as an empty numpy array.
- visualization.py:
   - It visualizes the minimum epsilon obtained for each episode. 

## Heuristics


## Qlearning

Please find the readme.md in the Qlearning folder.

# 📃 License

Licensed under SNCF ©2021. See the license for the details.
