#Workspace Notes

####RAPM Cleanup
2014 columns are differently formatted.  
2014 xRAPM/ASPM are extraneous to this study.  
90s columns are extraneous to this study.  
Remove header columns.  

####Getting College Nodes

SELECT DISTINCT(COALESCE(college, "None")) FROM players_college
ORDER BY college

####Getting HS Nodes

SELECT state, city, hs, COUNT(1) FROM players_hs
GROUP BY state, city, hs
ORDER BY state, city, hs