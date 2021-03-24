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
# Development

## Preprocessing

- toJsonData.py: converts the data provided (transport plan & action/regulation) to json files and put them in usefulData folder.
- remarkable_points_restructured.py: converts the remarkable points to json file.
- get_lines.py: takes the original transport plan and gathers the data on lines J and L, and saves them in two separate files lineJ.json and lineL.json respectively.
- removeElement.py: deletes the unecessary data existing in files lineL.json and lineJ.json and creates new files lineL_preprocessed.json and lineJ_preprocessed.json.
- get_times.py: 
- get_act_regul_lines.py:
   - Takes the action/regulation json file and deletes the unecessary data.
   - Filters the action/regulation file by the data on lines J and L, and creates new json files act_regul_lineJ.json and act_regul_lineL.json respectively.
- stopRefAndLibelle.py:
   - Uses LineJ_preprocessed.json to create a lineJ_StopRefAndLibelle.csv file in usefulData, that gathers the identifiers (ref) of the stations without taking into consideration the crossing points.
   - Calls the RemarkablePoints.json in usefulData and finds the name of each station existing in lineJ_StopRefAndLibelle.csv, and adds the name next to the identifier. So, in the end, lineJ_StopRefAndLibelle.csv contains the station identifier and its name.
- stopRefAndLibelle_reduced.py: Removes all of the rows in lineJ_StopRefAndLibelle.csv containing station identifiers that do not end with "BV" or "00".
- extract_final_pdt.py:

## Heuristics


## Qlearning

Please find the readme.md in the Qlearning folder.

# 📃 License

Licensed under SNCF ©2021. See the license for the details.
