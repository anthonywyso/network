
####Getting College Nodes

SELECT DISTINCT(COALESCE(college, "None")) FROM players_college
ORDER BY college

####Getting HS Nodes

SELECT state, city, hs, COUNT(1) FROM players_hs
GROUP BY state, city, hs
ORDER BY state