#Workspace Notes

####RAPM Cleanup
2014 columns are differently formatted.  
2014 xRAPM/ASPM are extraneous to this study.  
90s columns are extraneous to this study.  
Remove header columns.  

####Getting College Nodes from network.sqlite

SELECT DISTINCT(COALESCE(college, "None")) FROM players_college
ORDER BY college

####Getting HS Nodes from network.sqlite

SELECT state, city, hs, COUNT(1) FROM players_hs
GROUP BY state, city, hs
ORDER BY state, city, hs

####Getting Edge Weights Players to Teams from nbadb.sqlite

WITH season_total AS
(
SELECT player_id, season, sum(g) AS total
FROM player_seasonlogs_total
WHERE team_id <> 'TOT'
GROUP BY season, player_id
)
SELECT p.player_id, p.team_id, p.season, 1.0* g / total AS team_tenure_pct
FROM player_seasonlogs_total AS p
JOIN season_total AS s
ON p.player_id = s.player_id AND p.season = s.season AND p.team_id <> 'TOT'
ORDER BY p.season DESC

####Getting Edge Weights Coaches to Teams from network.sqlite

SELECT season, MAX(game_number) AS gp
FROM team_gamelogs_basic
WHERE game_type = 'regular'
GROUP BY season

