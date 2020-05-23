class DoesNotExist(Exception):
	pass
class MultipleObjectsReturned(Exception):
	pass
class InvalidField(Exception):
	pass

class Student:
	def __init__(self,name,age,score):
		self.name=name
		self.age=age
		self.score=score
		self.student_id=None   
	
	def save(self):
		import sqlite3
		connection = sqlite3.connect("students.sqlite3")
		crsr = connection.cursor()
		crsr.execute("PRAGMA foreign_keys=on;")
		if self.student_id == None:
			sql_query = 'INSERT INTO Student(student_id,name,age,score) VALUES(Null,"{}",{},{})'.format(self.name,self.age,self.score)
			crsr.execute(sql_query)
			self.student_id = crsr.lastrowid
		else:
			sql_query = 'INSERT or REPLACE INTO Student(student_id,name,age,score) VALUES({},\'{}\',{},{})'.format(self.student_id,self.name,self.age,self.score)
			crsr.execute(sql_query)

		connection.commit()
		connection.close()

	@staticmethod
	def get(**kwargs):
		for key,value  in kwargs.items():
			if key not in ['student_id','name','age','score']:
				raise InvalidField
			out = read_data(f'SELECT * FROM Student WHERE {key}="{value}"')
				
		if (len(out) == 0):
			raise DoesNotExist
		elif (len(out)>1):
			raise MultipleObjectsReturned 
		else:
			s = Student(out[0][1],out[0][2],out[0][3])
			s.student_id=out[0][0]
			return s
	
	def delete(self):
		query='DELETE FROM Student WHERE student_id={}'.format(self.student_id)
		write_data(query)

def read_data(sql_query):
	import sqlite3
	connection = sqlite3.connect("students.sqlite3")
	crsr = connection.cursor() 
	crsr.execute(sql_query) 
	ans= crsr.fetchall()  
	connection.close() 
	return ans
	
def write_data(sql_query):
	import sqlite3
	connection = sqlite3.connect("students.sqlite3")
	crsr = connection.cursor() 
	crsr.execute("PRAGMA foreign_keys=on;") 
	crsr.execute(sql_query) 
	connection.commit() 
	connection.close()