
- [x] As a developer I want to use relative comparison of my tasks to estimate them on a floating point scale.
- [x] As a developer I want to know how many workdays I need for the remaining tasks based on my recent velocity.
- [x] As a developer I want to know a predicted completed date of my project. (official and personal holidays, days spend on other activities, free weekdays)
- [x] As a developer I want to automatically reformat the planning and estimation files
- [x] As a developer I want a list of completed dates per item (in the given orders)
- [x] As a developer I want to know a (kind of) confidence interval for the remaining workdays.
- [x] As a developer I want to know a confidence interval for the completed date of my project. (official and personal holidays, days spend on other activities)
- [x] As a developer I want to see a burn-down chart of the project history showing: [x] the past as a line [x] the future as confidence band [x] (longer) holidays
- [x] As a devleoper I want to specify the start date from which project duration is predicted
- [x] TaskIdConflictException should contain the conflicting task id and show it to the user
- [x] As a developer I want to predict completed dates and confidence intervals for various projects separately while organizing my tasks together.
- [x] Project column in planning task tables
- [x] As a developer I want to know the distribution of my relative estimation errors (-> to use in a monte carlo simulation ?)
- [x] What is the correct velocity ? 
        - average(estimate_i / workdays_i) for every completed task i
        - sum(estimate_i) / sum(workdays_i) for every completed task i
        - Answer: sum(estimate_i) / sum(workdays_i), because in the first version estimation-errors of small tasks have too much weight!
- [x] Only copy the 3 most recently completed reference stories of every estimation level into the estimation file
- [ ] Do not copy strongly mis-estimated stories as reference stories into the estimation file

- [ ] As a developer I want to see a chart of the time evolution of the confidence band for the predicted completion date per project
    - [ ] show at which points tasks have been added, removed (or changed -- difficult to record) in the project plan

- [ ] monte carlo simulation -> measurement of the probability distribution estimation error?
- [ ] Epic: make it work for a team