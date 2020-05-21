Q1 ='''SELECT d.id, d.fname FROM Director d
       WHERE NOT EXISTS(
       SELECT * FROM Movie m JOIN MovieDirector md 
       ON m.id=md.mid
       WHERE d.id=md.did AND m.year < 2000)
       AND EXISTS(
       SELECT * FROM Movie m JOIN MovieDirector md
       ON m.id=md.mid 
       WHERE d.id=md.did AND m.year > 2000) 
       ORDER BY d.id;'''

Q2 = '''SELECT fname,(
SELECT name FROM Movie JOIN MovieDirector 
ON `Movie`.id==`MovieDirector`.mid
WHERE MovieDirector.did=Director.id
ORDER BY rank DESC, name ASC LIMIT 1) AS name FROM Director
LIMIT 100;'''

Q3 = '''
SELECT * FROM Actor WHERE id NOT IN(
SELECT Actor.id
FROM Actor  JOIN Cast
ON `Actor`.id=`Cast`.pid
JOIN Movie  
ON `Movie`.id=`Cast`.mid
WHERE year BETWEEN 1990 AND 2000)
 ORDER BY Actor.id DESC LIMIT 100;'''