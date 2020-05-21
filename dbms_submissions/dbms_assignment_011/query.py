Q1 = """SELECT A.ID,A.FNAME,A.LNAME,A.GENDER 
        FROM ACTOR A JOIN CAST C ON A.ID=C.PID 
        JOIN MOVIE M ON M.ID=C.MID 
        WHERE M.NAME LIKE 'ANNIE%';"""
        
Q2 = '''SELECT M.ID,M.NAME,M.RANK,M.YEAR
        FROM MOVIE M JOIN MovieDirector MD ON MD.MID=M.ID
        JOIN DIRECTOR D ON D.ID=MD.DID
        WHERE D.FNAME='Biff' AND D.lname='Malibu'
        AND m.year in(1999,1994,2003)
        ORDER  BY M.rank DESC, M.year;'''
        
Q3 ='''SELECT YEAR,COUNT(ID) AS NO_OF_MOVIES 
      FROM MOVIE GROUP BY YEAR HAVING AVG(RANK) >
      (SELECT AVG(RANK)FROM MOVIE) ORDER BY YEAR ASC;'''

Q4 = '''SELECT m.id,m.name,m.year,m.rank
        from Movie m WHERE year=2001 and
        rank < (SELECT AVG(rank) from Movie WHERE year=2001)
        ORDER BY m.rank DESC LIMIT 10;'''

# Q5 = '''SELECT m.id AS movie_id,
#         (SELECT COUNT(A.ID)
#         FROM Actor a JOIN Cast c
#         ON pid=a.id AND mid=m.id 
#         WHERE a.gender='F') AS no_of_female_actors,
#         (SELECT COUNT(A.ID)
#         FROM Actor a JOIN Cast c
#         ON pid=a.id AND mid=m.id WHERE a.gender='M') AS no_of_male_actors
#         FROM Movie m ORDER BY m.id ASC LIMIT 100;'''  


# Q5 = '''SELECT M.id, (SELECT COUNT(gender) FROM Actor JOIN Cast ON id = pid AND M.id = mid WHERE gender = "F") AS no_of_female_actors, 
#         (SELECT COUNT(gender) FROM Actor JOIN Cast ON id = pid AND M.id = mid WHERE gender = 'M') AS no_of_male_actors
#         FROM Movie AS M
#         ORDER BY M.id ASC
#         LIMIT 100;'''

Q6 = '''
SELECT DISTINCT c.pid
FROM Cast c JOIN Movie m
ON c.mid=m.id
GROUP BY c.mid,c.pid
HAVING COUNT(DISTINCT c.role) > 1
ORDER BY c.pid
LIMIT 100;
'''

Q7 = '''SELECT fname,COUNT(fname) AS count FROM Director GROUP BY fname HAVING count > 1;'''

Q8 = '''SELECT d.id,d.fname,d.lname FROM Director d WHERE d.id IN
(SELECT d.id FROM CAST c JOIN MovieDirector md  JOIN Director d
 ON c.mid=md.mid WHERE d.id=md.did GROUP BY md.mid,md.did HAVing COUNT(pid)>=100) 
 AND d.id NOT IN 
 (SELECT d.id FROM CAST c JOIN MovieDirector md  JOIN Director d 
 ON c.mid=md.mid WHERE d.id=md.did GROUP BY md.mid,md.did HAVing COUNT(pid)<100);'''


# Q8 = '''SELECT DISTINCT D.id, D.fname, D.lname
#         FROM Director AS D
#         WHERE EXISTS(SELECT `Director`.id FROM Director JOIN MovieDirector ON `Director`.id = `MovieDirector`.did AND D.id = `MovieDirector`.did
#                      JOIN Cast ON `Cast`.mid = `MovieDirector`.mid
#                      GROUP BY `Director`.id, `MovieDirector`.mid
#                      HAVING COUNT(`Cast`.role) >= 100)
#         AND
#         NOT EXISTS(SELECT `Director`.id FROM Director JOIN MovieDirector ON `Director`.id = `MovieDirector`.did AND D.id = `MovieDirector`.did
#                    JOIN Cast ON `Cast`.mid = `MovieDirector`.mid
#                    GROUP BY `Director`.id, `MovieDirector`.mid
#                    HAVING COUNT(`Cast`.role) < 100)
#         GROUP BY D.id;'''