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


#### Implementation of reconciliation between files

For now we'll focus on what already matches and works, then we'll see if we can match the rest.

1. get the shared keys
2. find the IDs only in the provider records
3. find the IDs only in the ledger records

print the stats

Report the discrepancies finished at: 15:41


### 2 save states and reload them

So if i run it on 2026-03-01, I get this:
Reconciliation — 2026-03-01

IDs found on both sides: 1959
Needs attention:
  9 IDs only in ledger
  7 IDs only in provider
Records without an ID (not grouped):
  19 in provider
  18 in ledger

Only in provider:
  provider | ref=pt_2a60eb7ecb9c | id=pt_2a60eb7ecb9c | amount=€13.43 | time=2026-03-01T10:56:46+00:00 | merchant=DE BIJENKORF
  provider | ref=pt_3d505cc5bc55 | id=pt_3d505cc5bc55 | amount=€15.10 | time=2026-03-01T05:09:00+00:00 | merchant=UBER *TRIP
  provider | ref=pt_800c822a0a9f | id=pt_800c822a0a9f | amount=€157.00 | time=2026-03-01T11:19:55+00:00 | merchant=SODEXO CATERING
  provider | ref=pt_8dd22003be92 | id=pt_8dd22003be92 | amount=€44.62 | time=2026-03-01T21:04:01+00:00 | merchant=DE BIJENKORF
  provider | ref=pt_90633ee7dcbf | id=pt_90633ee7dcbf | amount=€68.53 | time=2026-03-01T16:03:25+00:00 | merchant=KLM ROYAL DUTCH
  provider | ref=pt_c06b0e609d12 | id=pt_c06b0e609d12 | amount=€3.31 | time=2026-03-01T16:14:50+00:00 | merchant=NS REIZIGERS
  provider | ref=pt_df0d2ed13680 | id=pt_df0d2ed13680 | amount=€3.84 | time=2026-03-01T00:17:48+00:00 | merchant=COOLBLUE

Only in ledger:
  ledger | ref=LG-4186360 | id=pt_110fb2650b9b | amount=€16.33 | time=2026-03-01T22:06:57+00:00 | merchant=Uber B.V.
  ledger | ref=LG-4186605 | id=pt_21c4b9fddb5b | amount=€31.36 | time=2026-03-01T17:19:03+00:00 | merchant=Adobe Systems Software Ireland Ltd
  ledger | ref=LG-4185563 | id=pt_3bf19a82f830 | amount=€8.85 | time=2026-03-01T20:15:24+00:00 | merchant=NS Reizigers B.V.
  ledger | ref=LG-4186591 | id=pt_40f0880c7eab | amount=€181.00 | time=2026-03-01T03:10:50+00:00 | merchant=Media Markt Saturn Holding Nederland
  ledger | ref=LG-4185855 | id=pt_411dbb2612ba | amount=€23.66 | time=2026-03-01T21:08:23+00:00 | merchant=Albert Heijn B.V.
  ledger | ref=LG-4185341 | id=pt_4686e4321d9e | amount=€60.00 | time=2026-03-01T23:29:36+00:00 | merchant=Adobe Systems Software Ireland Ltd
  ledger | ref=LG-4185388 | id=pt_56be544c5b80 | amount=€79.44 | time=2026-03-01T20:56:43+00:00 | merchant=Bolt Operations OU
  ledger | ref=LG-4185406 | id=pt_84f4f769b85c | amount=€22.98 | time=2026-03-01T16:34:33+00:00 | merchant=VodafoneZiggo Group B.V.
  ledger | ref=LG-4185104 | id=pt_9a054872ab1b | amount=€10.47 | time=2026-03-01T21:56:50+00:00 | merchant=KLM N.V.

Provider records without an ID:
  provider | ref=provider-2026-03-01.jsonl:11 | id=no ID | amount=€31.00 | time=2026-03-01T00:07:07+00:00 | merchant=ALBERT HEIJN 1372
  provider | ref=provider-2026-03-01.jsonl:39 | id=no ID | amount=€30.43 | time=2026-03-01T00:25:01+00:00 | merchant=BOLT.EU
  provider | ref=provider-2026-03-01.jsonl:82 | id=no ID | amount=€30.25 | time=2026-03-01T00:57:05+00:00 | merchant=SODEXO CATERING
  provider | ref=provider-2026-03-01.jsonl:208 | id=no ID | amount=€26.74 | time=2026-03-01T02:20:11+00:00 | merchant=AMZN MKTPLACE EU
  provider | ref=provider-2026-03-01.jsonl:230 | id=no ID | amount=€26.98 | time=2026-03-01T02:35:35+00:00 | merchant=GOOGLE *CLOUD
  provider | ref=provider-2026-03-01.jsonl:294 | id=no ID | amount=€2.49 | time=2026-03-01T03:13:29+00:00 | merchant=ATLASSIAN
  provider | ref=provider-2026-03-01.jsonl:366 | id=no ID | amount=€5.26 | time=2026-03-01T04:05:12+00:00 | merchant=MEDIAMARKT
  provider | ref=provider-2026-03-01.jsonl:798 | id=no ID | amount=€21.00 | time=2026-03-01T09:25:10+00:00 | merchant=ALBERT HEIJN 1372
  provider | ref=provider-2026-03-01.jsonl:838 | id=no ID | amount=€150.34 | time=2026-03-01T09:55:24+00:00 | merchant=ZIGGO
  provider | ref=provider-2026-03-01.jsonl:862 | id=no ID | amount=€63.57 | time=2026-03-01T10:13:28+00:00 | merchant=MEDIAMARKT
  provider | ref=provider-2026-03-01.jsonl:916 | id=no ID | amount=€5.00 | time=2026-03-01T10:54:30+00:00 | merchant=BOL.COM
  provider | ref=provider-2026-03-01.jsonl:1059 | id=no ID | amount=€249.00 | time=2026-03-01T12:30:54+00:00 | merchant=AMZN MKTPLACE EU
  provider | ref=provider-2026-03-01.jsonl:1176 | id=no ID | amount=€10.86 | time=2026-03-01T13:44:47+00:00 | merchant=COOLBLUE
  provider | ref=provider-2026-03-01.jsonl:1399 | id=no ID | amount=€31.16 | time=2026-03-01T16:42:02+00:00 | merchant=ALBERT HEIJN 1372
  provider | ref=provider-2026-03-01.jsonl:1607 | id=no ID | amount=€82.99 | time=2026-03-01T19:30:03+00:00 | merchant=IKEA AMSTERDAM
  provider | ref=provider-2026-03-01.jsonl:1794 | id=no ID | amount=€43.31 | time=2026-03-01T21:43:13+00:00 | merchant=MEDIAMARKT
  provider | ref=provider-2026-03-01.jsonl:1810 | id=no ID | amount=€17.17 | time=2026-03-01T21:57:26+00:00 | merchant=THUISBEZORGD.NL
  provider | ref=provider-2026-03-01.jsonl:1829 | id=no ID | amount=€63.15 | time=2026-03-01T22:14:52+00:00 | merchant=GOOGLE *CLOUD
  provider | ref=provider-2026-03-01.jsonl:1862 | id=no ID | amount=€45.20 | time=2026-03-01T22:36:29+00:00 | merchant=JUMBO SUPERMARKTEN

Ledger records without an ID:
  ledger | ref=LG-4184873 | id=no ID | amount=€249.00 | time=2026-03-01T12:32:49+00:00 | merchant=Amazon EU S.a.r.l.
  ledger | ref=LG-4185131 | id=no ID | amount=€2.49 | time=2026-03-01T03:14:44+00:00 | merchant=Atlassian Pty Ltd
  ledger | ref=LG-4185209 | id=no ID | amount=€45.20 | time=2026-03-01T22:37:43+00:00 | merchant=Jumbo Supermarkten B.V.
  ledger | ref=LG-4185228 | id=no ID | amount=€10.86 | time=2026-03-01T13:46:44+00:00 | merchant=Coolblue B.V.
  ledger | ref=LG-4185407 | id=no ID | amount=€31.00 | time=2026-03-01T00:07:15+00:00 | merchant=Albert Heijn B.V.
  ledger | ref=LG-4185440 | id=no ID | amount=€5.00 | time=2026-03-01T10:55:02+00:00 | merchant=bol.com B.V.
  ledger | ref=LG-4185523 | id=no ID | amount=€82.99 | time=2026-03-01T19:31:12+00:00 | merchant=IKEA B.V.
  ledger | ref=LG-4185536 | id=no ID | amount=€63.15 | time=2026-03-01T22:17:27+00:00 | merchant=Google Cloud EMEA Ltd
  ledger | ref=LG-4185591 | id=no ID | amount=€63.57 | time=2026-03-01T10:14:18+00:00 | merchant=Media Markt Saturn Holding Nederland
  ledger | ref=LG-4185700 | id=no ID | amount=€30.43 | time=2026-03-01T00:26:29+00:00 | merchant=Bolt Operations OU
  ledger | ref=LG-4185816 | id=no ID | amount=€17.17 | time=2026-03-01T21:59:26+00:00 | merchant=Takeaway.com Group B.V.
  ledger | ref=LG-4185968 | id=no ID | amount=€31.16 | time=2026-03-01T16:42:49+00:00 | merchant=Albert Heijn B.V.
  ledger | ref=LG-4186047 | id=no ID | amount=€30.25 | time=2026-03-01T00:58:22+00:00 | merchant=Sodexo Nederland B.V.
  ledger | ref=LG-4186203 | id=no ID | amount=€26.74 | time=2026-03-01T02:22:05+00:00 | merchant=Amazon EU S.a.r.l.
  ledger | ref=LG-4186319 | id=no ID | amount=€26.98 | time=2026-03-01T02:35:59+00:00 | merchant=Google Cloud EMEA Ltd
  ledger | ref=LG-4186539 | id=no ID | amount=€5.26 | time=2026-03-01T04:07:40+00:00 | merchant=Media Markt Saturn Holding Nederland
  ledger | ref=LG-4186763 | id=no ID | amount=€249.00 | time=2026-03-01T12:31:19+00:00 | merchant=Amazon EU S.a.r.l.
  ledger | ref=LG-4186819 | id=no ID | amount=€43.31 | time=2026-03-01T21:45:42+00:00 | merchant=Media Markt Saturn Holding Nederland


  If I run it on the second day:

  Reconciliation — 2026-03-02

IDs found on both sides: 1955
Needs attention:
  4 IDs only in ledger
  12 IDs only in provider
Records without an ID (not grouped):
  6 in provider
  6 in ledger

Only in provider:
  provider | ref=pt_110fb2650b9b | id=pt_110fb2650b9b | amount=€16.33 | time=2026-03-01T22:06:07+00:00 | merchant=UBER *TRIP
  provider | ref=pt_27c4d852592b | id=pt_27c4d852592b | amount=€174.90 | time=2026-03-01T23:59:59+00:00 | merchant=MICROSOFT*365
  provider | ref=pt_3bf19a82f830 | id=pt_3bf19a82f830 | amount=€8.85 | time=2026-03-01T20:14:59+00:00 | merchant=NS REIZIGERS
  provider | ref=pt_3df98724f98e | id=pt_3df98724f98e | amount=€26.74 | time=2026-03-02T06:35:49+00:00 | merchant=MEDIAMARKT
  provider | ref=pt_411dbb2612ba | id=pt_411dbb2612ba | amount=€23.66 | time=2026-03-01T21:07:09+00:00 | merchant=ALBERT HEIJN 1372
  provider | ref=pt_4686e4321d9e | id=pt_4686e4321d9e | amount=€60.00 | time=2026-03-01T23:28:57+00:00 | merchant=ADOBE SYSTEMS
  provider | ref=pt_56be544c5b80 | id=pt_56be544c5b80 | amount=€79.44 | time=2026-03-01T20:55:36+00:00 | merchant=BOLT.EU
  provider | ref=pt_684c737828f6 | id=pt_684c737828f6 | amount=€98.97 | time=2026-03-01T23:59:59+00:00 | merchant=ETOS 0917
  provider | ref=pt_724ca1763f2a | id=pt_724ca1763f2a | amount=€108.88 | time=2026-03-01T23:59:59+00:00 | merchant=AMZN MKTPLACE EU
  provider | ref=pt_a395d9c4cf75 | id=pt_a395d9c4cf75 | amount=€43.93 | time=2026-03-02T02:16:14+00:00 | merchant=ETOS 0917
  provider | ref=pt_dbe425f2bef2 | id=pt_dbe425f2bef2 | amount=€50.75 | time=2026-03-02T02:21:43+00:00 | merchant=SODEXO CATERING
  provider | ref=pt_e10563e318b1 | id=pt_e10563e318b1 | amount=€282.99 | time=2026-03-02T19:08:39+00:00 | merchant=DE BIJENKORF

Only in ledger:
  ledger | ref=LG-4188763 | id=pt_2a60eb7ecb9c | amount=€13.43 | time=2026-03-01T10:56:58+00:00 | merchant=De Bijenkorf B.V.
  ledger | ref=LG-4188404 | id=pt_31e33c1194c0 | amount=€218.19 | time=2026-03-02T23:32:06+00:00 | merchant=Albert Heijn B.V.
  ledger | ref=LG-4187131 | id=pt_7498a6ee7897 | amount=€13.61 | time=2026-03-02T08:38:16+00:00 | merchant=Uber B.V.
  ledger | ref=LG-4188056 | id=pt_c44a68a2ad27 | amount=€63.43 | time=2026-03-02T23:57:35+00:00 | merchant=Takeaway.com Group B.V.

Provider records without an ID:
  provider | ref=provider-2026-03-02.jsonl:622 | id=no ID | amount=€112.43 | time=2026-03-02T07:25:01+00:00 | merchant=NS REIZIGERS
  provider | ref=provider-2026-03-02.jsonl:767 | id=no ID | amount=€108.52 | time=2026-03-02T09:12:53+00:00 | merchant=JUMBO SUPERMARKTEN
  provider | ref=provider-2026-03-02.jsonl:1329 | id=no ID | amount=€8.31 | time=2026-03-02T15:58:24+00:00 | merchant=ATLASSIAN
  provider | ref=provider-2026-03-02.jsonl:1375 | id=no ID | amount=€12.00 | time=2026-03-02T16:36:49+00:00 | merchant=ETOS 0917
  provider | ref=provider-2026-03-02.jsonl:1432 | id=no ID | amount=€10.83 | time=2026-03-02T17:18:40+00:00 | merchant=MEDIAMARKT
  provider | ref=provider-2026-03-02.jsonl:1538 | id=no ID | amount=€50.20 | time=2026-03-02T18:41:54+00:00 | merchant=TRAVELCARD BV

Ledger records without an ID:
  ledger | ref=LG-4186922 | id=no ID | amount=€50.20 | time=2026-03-02T18:43:48+00:00 | merchant=Travelcard B.V.
  ledger | ref=LG-4187013 | id=no ID | amount=€8.31 | time=2026-03-02T16:00:02+00:00 | merchant=Atlassian Pty Ltd
  ledger | ref=LG-4187211 | id=no ID | amount=€112.43 | time=2026-03-02T07:25:11+00:00 | merchant=NS Reizigers B.V.
  ledger | ref=LG-4187764 | id=no ID | amount=€12.00 | time=2026-03-02T16:39:29+00:00 | merchant=Etos B.V.
  ledger | ref=LG-4188262 | id=no ID | amount=€108.52 | time=2026-03-02T09:13:05+00:00 | merchant=Jumbo Supermarkten B.V.
  ledger | ref=LG-4188385 | id=no ID | amount=€10.83 | time=2026-03-02T17:19:19+00:00 | merchant=Media Markt Saturn Holding Nederland



Are there any doubles amongst these, and which? Well codex found these:

found six repeated transaction IDs across the two reports’ one-sided lists. In each case, the amount is the same and the record appears on opposite sides on the two dates:
| Transaction ID | March 1 report | March 2 report | Amount |
|---|---|---|---:|
| `pt_2a60eb7ecb9c` | Provider only | Ledger only | €13.43 |
| `pt_110fb2650b9b` | Ledger only | Provider only | €16.33 |
| `pt_3bf19a82f830` | Ledger only | Provider only | €8.85 |
| `pt_411dbb2612ba` | Ledger only | Provider only | €23.66 |
| `pt_4686e4321d9e` | Ledger only | Provider only | €60.00 |
| `pt_56be544c5b80` | Ledger only | Provider only | €79.44 |


These look like date-boundary discrepancies: the same transaction is missing from one side’s March 1 comparison, then appears on the other side’s March 2 comparison. So the problem seems to be a shift in date.
For example:

 provider | ref=pt_2a60eb7ecb9c | id=pt_2a60eb7ecb9c | amount=€13.43 | time=2026-03-01T10:56:46+00:00 | merchant=DE BIJENKORF
 ledger | ref=LG-4188763 | id=pt_2a60eb7ecb9c | amount=€13.43 | time=2026-03-01T10:56:58+00:00 | merchant=De Bijenkorf B.V.

same reference, same amount, and almost the same time and same merchant.

But no doubles on the same side then.


# COFFEE BREAK AT 16:15 (1 hour an 45 min in)
# STARTED AGAIN AT 16:45 

To get the states:

If an issue appears on march the second, that wasn't on march the first it is new -> add to the report

An issue on both, but with changed details, has changed

If an issue was on march the first, but not on march the second, can you assume it was solved or is it just an added issue?

so new, resolved or changed.

And also there might be entries that bounced to the next day (there are datapoints to confirm this), so you kind of want to do a rerun of everything, also what is saved in the state.

Misunderstanding about the state -> A new state is created each run
NO, the state is updated each run and built upon.

So find today's issues
Add the issues to the list
Remove it when it can be fixed (based on new input)
Save the update list.

Current attempt at implementing states:

