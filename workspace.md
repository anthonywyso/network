#Planning

##Timeline
- 11/03 -- TODO plan project
	- Built general data model for graph network
	- Need to flesh out model to account for time/duration information
- 11/04 -- TODO get all basic data to build network
	- Scraped hs/college data for players/coaches
	- Found prior work on time series
- 11/05 -- TODO gather college/pro duration data for players/coaches; clean data; process into Neo4j/NetworkX/GraphLab/Gephi
	- pass
- 11/06 -- TODO 
	- pass
- 11/07 -- TODO Have a working database in Neo4j
	- pass
- 11/08 -- TODO 
	- pass
- 11/09 -- TODO 
	- pass
- 11/10 -- TODO 
	- pass
- 11/11 -- TODO 
	- pass
- 11/12 -- TODO 
	- pass
- 11/13 -- TODO 
	- pass
- 11/14 -- TODO 
	- pass

##Data Pipeline
Scrapy/Python --> csv --> clean --> Neo4j --> Maybe Gephi/Graphlab

Scrapy Crawl

- Players -- 2014 to 1994
    - http://www.basketball-reference.com/leagues/NBA_2014_totals.html
    - http://www.basketball-reference.com/leagues/NBA_1994_totals.html
- Coaches -- All
    - http://www.basketball-reference.com/coaches/
- Institutions
- Transactions

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
4. (High School) {name, id} -- DONE 11/04
5. (Professional) Team {name, id}
6. (Award) {name}

Relationships

1. [ATTENDED_COLLEGE]->(College)
2. [ATTENDED_HIGHSCHOOL]->(High School)
3. [PLAYS_FOR]->(Team)
4. [PLAYED_IN]->(Game)
5. [AWARDED]->(Award)

???

1. Time-series


##What does this solve?
Find the best coach/development staff for certain types of players (traditional 1-5 positions; roles) -- http://www.wired.com/2013/03/basketballs-hidden-positions/

Year-end awards (NBA-All Team Honors, DPOY, MVP, )

http://maxdemarzi.com/2012/05/31/key-players/#more-998
http://maxdemarzidotcom.files.wordpress.com/2012/05/key_players_chart1.jpg?w=580&h=341

- Disrupt: Who should be removed from the network to disrupt it?
- Protect: Who should be protected in order to keep the network functioning?
- Influence: Who should be influenced in order to change social opinion?
- Learn: Who should be questioned in order to know what is going on?
- Redirect: Who should be moved to alter social flows?

##Prior Work
- http://edschembor.github.io/blog/index.html
- http://thecodebarbarian.wordpress.com/2014/02/14/crunching-30-years-of-nba-data-with-mongodb-aggregation/
- http://www.neo4j.org/graphgist?8493604
- https://github.com/SocioPatterns/neo4j-dynagraph/wiki/Representing-time-dependent-graphs-in-Neo4j

##Presenting/hosting Project
http://www.graphenedb.com/pricing.html

##Outstanding Questions/Obstacles
1. How to model time/duration in graph db (such as isolating the time when someone starts and ends playing for a team)
	- Weighted edges (days involved with team)
2. Determine weights/size of nodes