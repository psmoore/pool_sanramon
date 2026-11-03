# City of San Ramon Aquatics — unofficial preview

A mock-up of [the City of San Ramon's Aquatics pages](https://www.sanramon.ca.gov/our_city/departments_and_divisions/parks_community_services/aquatics)
(Aquatics, San Ramon Olympic Pool & Aquatic Park, Dougherty Valley Aquatic Center, Lap Swim, Teams & Other Services, Classes &
Camps, Pool Closure Dates) with both aquatic centers on one live [Pool Relay](https://www.poolrelay.com) schedule. Not operated
by or affiliated with the City of San Ramon.

No schedule is typed into the pages. Lap swim hours, practices, classes and closures are filled by `finder.js` from the live
Pool Relay views; `build.py` holds only prices, ages, policies and facts about the water.

- `build.py`: generates the seven pages.
- `finder.js`: `#finder` (swim-now board), `#today`, `#week`, and `data-live` elements (`hours`, `when`, `exceptions`,
  `closures`, `swims`). `data-group` picks a program by its Pool Relay group; `data-pool="srop|dvac"` reads one program at both centers.
- Pool Relay views: `crpwBd7tJOeik4pmuAR3ID` (San Ramon Olympic Pool & Aquatic Park, lane by lane),
  `v0jSpnBF5QDS1Yb8kKWGnq` (Dougherty Valley Aquatic Center, lane by lane).
