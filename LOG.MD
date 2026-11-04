# Case Study Log Technical Assignment - Deloitte Software Developer
Start time: Wednesday 04-11-2026 at 14:30
Approx duration of the exercise: 3h
Deadline 5 November


## Initial setup run
Chose the Python starter, moved it to the repo root. Set up a virtual environment, added the recon command, configured debugging, and fixed file paths after the move. Added generated files to .gitignore.


## Action plan
1. Go through the repo and the data
2. Understand Assignement and create tasks to focus on
3. Log as you go


## My take on the assignement

As is already stated start with this order:
1. Report discrepancies
2. Safe a state after run
3. Report only what changed -> The 2-day run (using previous state)
4. Re-running must be safe



### 1 Report on discrepancies
Report discrepancies — transactions present on one side but not the other, and transactions on both sides with differing amounts.

A possible example of this:
    Reconciliation — 2026-03-01

    950 transactions agree
    12 need attention:
        5 only in ledger
        3 only in provider
        2 with different amounts
        2 uncertain matches


Clarification of what they mean with between raports and states between runs:

The daily report is shown in the commandline directly. And it reports directly the stats and the transactions. (see the overview above).

the states are between dates:

So 
1. First run on day 1, compare files, prints report and saves the findings as a state
2. Next day, run it again. Compares files, then compares those findings with the findings of march 2nd the report can show what is new and whats been resolved.


### 2 save states and reload them