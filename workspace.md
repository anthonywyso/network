#Workspace Notes

####RAPM Cleanup
2014 columns are differently formatted.  
2014 xRAPM/ASPM are extraneous to this study.  
90s columns are extraneous to this study.  
Remove header columns.  

####Getting College Nodes
CREATE VIEW IF NOT EXISTS colleges AS
SELECT COALESCE(college, "None") AS college, COUNT(1) AS players_attended FROM players_college
GROUP BY college

####Getting HS Nodes
CREATE VIEW IF NOT EXISTS high_schools AS
SELECT state, city, hs, COUNT(1) AS players_attended FROM players_hs
GROUP BY state, city, hs
ORDER BY state, city, hs

####Getting Edge Weights Players to Teams
- Games played for team / total games played
- Describes portion of (playing) season with team
- Does not account for time when players were on a team but did not play in games
- Over values players who were on a team for few games but played in all of them
- Does not account for actual timeline of games

CREATE VIEW IF NOT EXISTS players_seasonlog_tenures AS
WITH season_total AS
(
SELECT player_id, season, sum(g) AS total
FROM players_seasonlog_totals
WHERE team_id <> 'TOT'
GROUP BY season, player_id
)
SELECT p.player_id, p.team_id, p.season, 1.0* g / total AS team_tenure_pct
FROM players_seasonlog_totals AS p
JOIN season_total AS s
ON p.player_id = s.player_id AND p.season = s.season AND p.team_id <> 'TOT'
ORDER BY p.season DESC

####Getting Edge Weights Coaches to Teams
- Games coached / total games in season
- Describes portion of season coached
- Does not account for canceled games/actual game count #
	- Need to scrape individual season pages for more granular game count #
- Does not account for actual timeline of games

CREATE VIEW IF NOT EXISTS coaches_seasonlog_tenures AS
SELECT c.id AS coach_id, c.team_id, c.season, 1.0 * c.gp / l.gp AS team_tenure_pct
FROM coaches_seasonlog_totals AS c
JOIN league_seasonlog AS l
ON c.season = l.season
ORDER BY c.id

####Getting Edge Weights Players to Pro coaches
- Find intersection of players and coaches
- Describes portion of player's season impacted by a certain coach
- Does not necessarily describe the NBA season (82 games)
- Does not account for actual timeline of games (actual tenures might have been staggered with no intersection)

CREATE VIEW IF NOT EXISTS player_coach_tenures AS
SELECT player_id, coach_id, c.season, p.team_tenure_pct * c.team_tenure_pct AS player_coach_tenure_pct
FROM players_seasonlog_tenures AS p
JOIN coaches_seasonlog_tenures AS c
ON p.team_id = c.team_id AND p.season = c.season AND p.team_id <> 'TOT'
ORDER BY c.season DESC

- Sanity Check

WITH impact AS (
SELECT player_id, season, SUM(player_coach_tenure_pct) AS impact
FROM player_coach_tenures
GROUP BY player_id, season
ORDER BY season DESC, player_id
)
SELECT *
FROM impact
WHERE impact <> 1 and season > 1990

SELECT player_id, coach_id, p.team_id, p.season, p.team_tenure_pct, c.team_tenure_pct, p.team_tenure_pct * c.team_tenure_pct
FROM players_seasonlog_tenures AS p
JOIN coaches_seasonlog_tenures AS c
ON p.team_id = c.team_id AND p.season = c.season AND p.team_id <> 'TOT'
WHERE p.player_id = 'beckemo01' AND p.season = 1947

"collija04","2013","0.9897304236200255"
"josepkr01","2013","0.9926829268292683"
"crawfjo02","2013","0.9952961672473868"
"varnaja01","2013","0.9953095684803002"
"mcguido01","2013","0.99906191369606"

####Attributing Player RAPM to Player id
10492 total records

Confirm all rapm records associated with at least 1 player id
WITH z AS (
SELECT COALESCE(p.id, 0) AS id, pr.name, pr.season
FROM players_rapm AS pr
LEFT JOIN players AS p
ON pr.name = p.name
)
SELECT DISTINCT(name) 
FROM z
WHERE id = 0

"Sergey Bazarevich" -- Sergei Bazarevich
"Amare Stoudemire" -- Amar'e Stoudemire
"Jeff Pendergraph" -- Jeff Ayres
"Ishmael Smith" -- Ish Smith // Sometimes Ish Sometimes Ishmael
"Dennis Schroeder" -- Dennis Schröder
Larry Krystkowiak, 1991 -- Playoffs only
Dwayne Jones, 2013 -- Playoffs only
Jeff Taylor, 2013/14 -- Jeffery Taylor

id, name, pos
bazarse01, Sergey Bazarevich, G
pendeje02, Jeff Pendergraph, F
schrode01, Dennis Schroeder, G
smithis01, Ishmael Smith, G
stoudam01, Amare Stoudemire, F-C

SELECT COALESCE(p.player_id, 0) AS id, pr.*, p.*
FROM players_rapm AS pr
LEFT JOIN players_seasonlog_totals AS p
ON pr.name = p.player AND pr.season = p.season AND p.record_type = 'full'
WHERE id = 0
ORDER BY id

UPDATE players_rapm
SET name = "Jeffery Taylor"
WHERE name = "Jeff Taylor"

Must account for duplicate names, pair to unique player_id.
CREATE VIEW rapm_duplicates AS
WITH z AS (
SELECT pr.*, p.*, COUNT(*) AS cnt
FROM players_rapm AS pr
JOIN players_seasonlog_totals AS p
ON pr.name = p.player AND pr.season = p.season AND p.record_type = 'full'
GROUP BY pr.name, pr.season
)
SELECT *
FROM z
WHERE cnt > 1

Charles Smith -- 1991, 1996
Chris Johnson -- 2013
Marcus Williams -- 2008, 2009
Michael Smith -- 1995
Tony Mitchell -- 2014

SELECT pr.name, pr.season, p.player_id, *
FROM players_rapm AS pr
JOIN players_seasonlog_totals AS p
ON pr.name = p.player AND pr.season = p.season AND p.record_type = 'full'

Had to manually reconcile these ambiguous names based on minutes played & poss.