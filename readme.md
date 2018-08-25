# Co-occurrence Analysis

It analyze the tweets and shows co-occurrence of terms with respect to some other terms.
Put tweets file in 'co_occurrence_analysis/data' folder named '_stream.jsonl' file.

## Install dependencies
Python3 is pre-requisite to this program.
There are some open-source python libraries used, which are listed in requirements.txt file.
YOu can install those packages by running `pip3 install -r requirements.txt`.


## Analyze
For analyze, run below command which loads all the tweets and analyze them. Provide your term as 1st argument.
If you don't provide the term then it expoorts all the pairs.

`python3 analyze.py <term> `<br /><br />


## Exported Data
After analysis if you don't provide any term this program exports all the pairs in the file name 'all_co_occurrences.csv'
otherwise if some <term> is provided then it filters those pairs containing that term only and the export file name would be
'<term>_co_occurrence.csv'.

It also generate a Gephi supported Network file at location 'data/co_occurrence.graphml'.


## Sigmajs Visualization

1. Open Gephi and install SigmaExporter plugin. Tools > Plugin > Available Plugins > (search for SigmaExporter).
2. Open the above created gephi network file 'data/co_occurrence.graphml' in Gephi.
3. Export as Sigmajs template i-e; File > Export > Sigmajs templa > (give a folder where it exports in filrst big field where "Browse .." button is) > (hit ok)
4. Goto the exported folder > Network
5. Execute `python3 -m http.server 9999`
6. Open browser and go to `localhost:9999`
7. You can interact with the graph interactively.
 Search terms that you wan on the left side panel.
 On right side you will see all the terms in current shortlisted graph.
 In that way you can play a analyze ;)

