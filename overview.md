#Planning Overview

##Timeline
- 11/03 -- TODO plan project
	- Built general, "flat" data model for graph network @done
	- Flesh out "layered" data model to account for time/duration information @done
- 11/04 -- TODO get all basic data to build network
	- Scrape hs data for players @done
	- Scrape college data for players @done
	- Scrape data for nba coaches @done
	- Research time series representation for graph networks @done
- 11/05 -- TODO gather team tenure data for players/coaches; clean data
 	- Clean hs/college data @done
	- Scrape nba coach seasonlog data @done
	- Clean nba coach seasonlog data @done
	- Clean nba coach awards data @done
	- Scrape RAPM data @done
	- Clean RAPM data @done
	- Get total number games per nba season @done
	- Build edges nba coaches to team (Aggregate data on tenure; weigh on seasons) @done
	- Scrape player awards data @postponed
- 11/06 -- TODO aggregate data; process into Neo4j/NetworkX/GraphLab/Gephi
	- Build edges nba coaches to team (Aggregate data on tenure; weigh on seasons) @done
	- Build edges players to nba coaches @done
	- Build edges players to college (tenure) @postponed
	- Build edges players to hs (tenure) @postponed
	- Scrape college coaches (http://www.sports-reference.com/cbb/coaches/) @postponed
	- Build edges players to college coaches @postponed
- 11/07 -- TODO Have a working database in Neo4j; compute analytics on network
	- Weigh player nodes -- RAPM -- Needs additional cleaning @done
	- Build single season network amongst players and pro coaches @done
	- Calculate analytics on single season network @done somewhat
	- Put single season players and pro coaches into Neo4j @done
- 11/10 -- TODO Research/better understand graph analytics; get college nodes
	- Rescrape for college id -- needed for Neo4j College node property @postponed (DONE 11/13)
	- Stanford's Social & Information Network Analysis course -- Intro @done
	- Stanford's Social & Information Network Analysis course -- Network Properties @done
	- Consider reorganizing nodes -- use only people and connect them with directed nodes "played_with", "coached", "assistant_coached"
	- Rethink questions -- analyze network evolution; network influence on behavior change
	- Exploratory analysis on coach's impact on players' RAPM over time @done
	- Troubleshoot sqlite3 -- cannot use "WITH" @done
- 11/11 -- TODO Apply analysis metrics to single season
	- Research PageRank @done
	- Incorporate player RAPM to edge weights @done
	- Calculate mean, sum of player RAPM edge weights @done
	- PageRank networkx for 2014 -- Weigh on Player values @done
	- Implement Time Weighted PageRank @postponed
	- Stanford's SINA -- Cascade Behaviors & Flow @done
- 11/12 -- TODO Presentation; Coach Analysis with traditional statistics
	- Compare coaches for player rapm in rookie season @done
		- Query rookie seasons @done
		- Visualize distribution of rookie season performances @done
		- KS-test on rookie seasons with various coaches @done
		- t-test on rookie seasons with various coaches @done
		- Code into py file @done
	- Compare coaches for player rapm through sophomore season @postponed
		- Query sophomore seasons
		- Query difference in performance between rookie/soph seasons
- 11/13 -- TODO Presentation; Extract pagerank, clusters from network
	- Get all players, coaches, RAPM scores from database @done
	- Put nodes into Gephi @done
	- Run analysis in Gephi @done
	- Review Gephi analysis with Jon/Zach @done
	- Scrape player gamelogs for more granular relationship weights (find how many games together) @kicked off
- 11/14 -- TODO 
	- Export Gephi analytics
	- NetworkX analysis with player-player connections
	- Dump nodes and edges into Neo4j to allow ppl to query for multiple connections 

##Data Pipeline
Scrapy/Python --> csv --> clean --> Neo4j --> Maybe Gephi/Graphlab

Scrapy Crawl

- Players -- All
    - http://www.basketball-reference.com/players/
- Coaches -- All
    - http://www.basketball-reference.com/coaches/
- Institutions
- Transactions
- Awards
	- http://www.basketball-reference.com/awards/

py2neo Neo4j import

- from py2neo import neo4j
- Cypher queries to post data into database
- http://nigelsmall.com/py2neo/1.6/  
- http://neo4j.com/developer/guide-importing-data-and-etl/

####Current Data Structure
1. Player Pages
    - Name
    - High school (name, location, link, duration)
    - College (name, location, link, duration)
    - Professional Teams (name, location, link, duration)
    - Transactions (type, date, institutions involved)
    - Draft -- maybe
    - NBA Debut -- maybe
    - Position
    - All NBA status
2. Coach Pages
    - Name
    - High school
    - College
    - Professional Teams
    - Transactions
    - Draft
3. Institution Pages
    - Name
    - Location
4. Transaction Pages
    - Trade
    - Free Agency
    - Attended school
    - Played for
    - Coached for

####Graph Data Model
http://neo4j.com/developer/guide-data-modeling/

- Nodes -- "entities with unique conceptual identity"
	- RDB rows as nodes
- Labels -- Group nodes together (represent quality/weight)
	- RDB tables as labels
- Relationships -- Describe interactions between nodes
	- RDB joins as relationships
- Properties -- Describe nodes & relationships


Nodes/Labels -- Properties

1. (Player) {name, id} -- DONE 11/04
2. (Coach) {name, id} -- DONE 11/04
3. (College) {name, id} -- DONE 11/04
4. (High School) {name, city, state, id} -- DONE 11/04
5. (Professional) Team {name, id} -- DONE 11/05
6. (Award) {name} ?? -- maybe use this as a node property

Relationships

1. [ATTENDED_COLLEGE]->(College)
2. [ATTENDED_HIGHSCHOOL]->(High School)
3. [PLAYS_FOR]->(Team)
4. [PLAYED_IN]->(Game)
5. [AWARDED]->(Award)

???

1. Time-series


##What does this solve?
1. Find the best coach/development staff for certain types of players (traditional 1-5 positions; roles) -- http://www.wired.com/2013/03/basketballs-hidden-positions/

2. Find value of relationships amongst players, coaches, teams, institutions.

http://maxdemarzi.com/2012/05/31/key-players/#more-998
http://maxdemarzidotcom.files.wordpress.com/2012/05/key_players_chart1.jpg?w=580&h=341

- Disrupt: Who should be removed from the network to disrupt it?
- Protect: Who should be protected in order to keep the network functioning?
- Influence: Who should be influenced in order to change social opinion?
- Learn: Who should be questioned in order to know what is going on?
- Redirect: Who should be moved to alter social flows?

http://www.infoq.com/articles/data-modeling-graph-databases

##Prior Work
- http://edschembor.github.io/blog/index.html
- http://thecodebarbarian.wordpress.com/2014/02/14/crunching-30-years-of-nba-data-with-mongodb-aggregation/
- http://www.neo4j.org/graphgist?8493604
- https://github.com/SocioPatterns/neo4j-dynagraph/wiki/Representing-time-dependent-graphs-in-Neo4j
- http://maxdemarzi.com/2014/01/31/neo4j-spatial-part-1/
- http://www.lyonwj.com/mapping-the-worlds-airports-with-neo4j-spatial-and-openflights-part-1/

##Presenting/hosting Project
http://www.graphenedb.com/pricing.html

##Analysis Tools
- Research NetworkX (python) vs igraph (c) vs graph-tools (c++) vs snap.py (c++)

##Analytics/Metrics
####Graph
- PageRank -- Compute the coach impact/value based on player values
	- http://www.cs.princeton.edu/~chazelle/courses/BIB/pagerank.htm
	- http://www-rohan.sdsu.edu/~gawron/python_for_ss/course_core/book_draft/Social_Networks/Networkx.html
	- http://healthyalgorithms.com/tag/networkx/
	- http://stackoverflow.com/questions/9136539/how-to-weighted-edges-affect-pagerank-in-networkx
	- http://www.cs.uic.edu/~xli3/wi05.pdf
	- Time Weighted PageRank -- Uses decay factor for "votes" based on when connection is formed relative to "now"
- Flow -- To find the maximum path of value
	- Might be able to figure out how players can maximize their performance through coaches
- Connectivity -- To find the most connected nodes

######Network Degree	
- Modularity Class (Adjust resolution to alter communities)
- PageRank (Should identify most connected individuals)

######Node Overview
- Eigenvector Centrality

######Edge Overview
- Avg Path Length
- Edge Betweenness
- Link Communities
	
	
####Traditional Statistics
- KS-test
	- http://stats.stackexchange.com/questions/57885/how-to-interpret-p-value-of-kolmogorov-smirnov-test-python

##Outstanding Questions/Obstacles
1. How to model time/duration in graph db (such as isolating the time when someone starts and ends playing for a team)
	- Seperate into time frames (year) and connect those frames with edges
2. How to determine edge weights of
	- Time together (games/days/seasons), maybe add time-based decay
3. How to determine weights of player nodes
	- RAPM (http://stats-for-the-nba.appspot.com/)
	- xRAPM
	- Team MoV
	- Year-end awards (NBA-All Team Honors, DPOY, MVP, ROY, SOY, MIP)
	- http://www.basketball-reference.com/friv/
	- http://basketball.realgm.com/nba/awards/by_type/All-NBA-First-Team/12
4. How to determine weights of coach nodes
	- Team wins, championships
5. Do not use institutions, teams as intermediate nodes
	- Connect players, coaches, teams, institutions directly
6. How to represent multiple, disjunct relationships amongst nodes
	- ????
7. Relationships/impact don't go away, should edge weights be aggregated frame-over-frame?
8. Get exact player/coach intersections rather than the rough season estimation/calculation