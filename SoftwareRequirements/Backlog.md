
- [ ] Epic: make it work for a team
  - [ ] Extract working days and holidays to file
  - [ ] Each developer must have her own file of working days and holidays
  - [x] velocity for prediction should be scaled down to v * (N-k) / N when k developers are absent
  - [x] velocity must be determined as v = Sum(Points) / Sum(person-working-days while issues in progress)

- [ ] As a developer I want to see a chart of the time evolution of the confidence band for the predicted completion date per project
  - [ ] report should log its current prediction to a file per project in a plottable format
  - [ ] show at which points tasks have been added, removed (or changed -- difficult to record) in the project plan

- [ ] Get Information from Jira
  - [ ] Get new Issues from Jira and automatically add them with creation date
  - [ ] Get closed (i.e. removed) issues from Jira and move them to removed with removed date
  - [ ] Get Started and Fixed data from Jira
  - [ ] (Upload estimation to Jira?)

- [ ] Do not copy strongly mis-estimated stories as reference stories into the estimation file

- [ ] monte carlo simulation -> measurement of the probability distribution estimation error?
