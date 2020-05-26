class DoesNotExist(Exception):
	pass

class MultipleObjectsReturned(Exception):
	pass

class InvalidField(Exception):
	pass

class Student:
    def __init__(self, name, age, score):
        self.name = name
        self.student_id = None
        self.age = age
        self.score = score
    
    def __repr__(self):
        return "Student(student_id={0}, name={1}, age={2}, score={3})".format(
            self.student_id,
            self.name,
            self.age,
            self.score)
    
    @staticmethod
    def get(**kwargs):
        for key, value in kwargs.items():
            if key not in ("student_id", "name", "age", "score"):
                raise InvalidField
        sql_query = read_data(f"SELECT * FROM Student WHERE {key} = '{value}'")
        
        if len(sql_query) == 0:
            raise DoesNotExist
        elif len(sql_query) > 1:
            raise MultipleObjectsReturned
        else:
            ans = Student(sql_query[0][1], sql_query[0][2], sql_query[0][3])
            ans.student_id = sql_query[0][0]
            return ans

    def save(self):
        import sqlite3
        conn = sqlite3.connect("selected_students.sqlite3")
        c = conn.cursor() 
        c.execute("PRAGMA foreign_keys=on;")
        
        if self.student_id == None:
            c.execute(f"INSERT INTO Student (name, age, score) values ('{self.name}', {self.age}, {self.score})")        
            self.student_id = c.lastrowid
        
        elif c.execute(f"SELECT {self.student_id} not in (SELECT student_id FROM Student) FROM Student"):
            c.execute(f"REPLACE INTO Student (student_id, name, age, score) values ({self.student_id}, '{self.name}', {self.age}, {self.score})")        
            
        else:
            c.execute(f"UPDATE Student SET name = '{self.name}', age = {self.age}, score = {self.score} WHERE student_id = {self.student_id}")
        
        conn.commit() 
        conn.close()
        
    def delete(self):
        write_data(f"DELETE FROM Student WHERE student_id = {self.student_id}")

    @staticmethod       
    def filter(**kwargs):
        temp_list=[]
        final_list=[]
        #q=None
        iteration=1
        for key,value in kwargs.items():
            def key_fun(key):

                switcher={
                    'age': 'age={}'.format(value),
                    'age__lt': 'age < {}'.format(value),
                    'age__lte':'age <= {}'.format(value),
                    'age__gt': 'age > {}'.format(value),
                    'age__gte':'age >= {}'.format(value),
                    'age__neq': 'age <> {}'.format(value),
                    
                    'score': 'score={}'.format(value),
                    'score__lt': 'score < {}'.format(value),
                    'score__lte':'score <= {}'.format(value),
                    'score__gt': 'score > {}'.format(value),
                    'score__gte':'score >= {}'.format(value),
                    'score__neq': 'score <> {}'.format(value),
                    
                    'student_id': 'student_id={}'.format(value),
                    'student_id__lt': 'student_id < {}'.format(value),
                    'student_id__lte':'student_id <= {}'.format(value),
                    'student_id__gt': 'student_id > {}'.format(value),
                    'student_id__gte':'student_id >= {}'.format(value),
                    'student_id__neq': 'student_id <> {}'.format(value),
                    
                    'name': 'name=\'{}\''.format(value),
                    'name__neq': 'name <> \'{}\''.format(value),
                    'name__contains':'name like \'%{}\''.format(value)
                }
            
            
                condition=switcher.get(key)
                if(condition==None):
                    raise InvalidField
                query='SELECT * FROM Student WHERE {}'.format(condition)
                return query
            
            if key in['age__in','score__in','student_id__in','name__in']:
                value=tuple(value)
                query='SELECT * FROM Student WHERE {} in {}'.format(key[0:-4],value)
            else:
                query=key_fun(key)

            results=read_data(query)
            for i in results:
                if iteration==1:
                    temp_list.append(i)
                else:
                    temp_list=set(temp_list)
                    results=set(results)
                    temp_list=temp_list.intersection(results)

            iteration+=1
        for i in temp_list:
            student_obj=Student(i[1],i[2],i[3])
            student_obj.student_id=i[0]
            final_list.append(student_obj)
        return final_list







    # @staticmethod    
    # def filter(**kwargs):
    #     for key, value in kwargs.items():
    #         keys = key
    #         values = value
            
    #     x = keys.split("__")
        
    #     if x[0] not in ("student_id", "name", "age", "score"):
    #         raise InvalidField
            
    #     if keys in ("student_id", "name", "age", "score"):
    #         sql_query = read_data(f"SELECT * FROM Student WHERE {keys} = '{values}'")
    #     else:
                
    #         keys = keys.split("__")
                
    #         if keys[1] == "lt":
    #             sql_query = read_data(f"SELECT * FROM Student WHERE {keys[0]} < '{values}'")
                    
    #         elif keys[1] == "lte":
    #             sql_query = read_data(f"SELECT * FROM Student WHERE {keys[0]} <= '{values}'")
                    
    #         elif keys[1] == "gt":
    #             sql_query = read_data(f"SELECT * FROM Student WHERE {keys[0]} > '{values}'")
                    
    #         elif keys[1] == "gte":
    #             sql_query = read_data(f"SELECT * FROM Student WHERE {keys[0]} >= '{values}'")
                    
    #         elif keys[1] == "neq":
    #             sql_query = read_data(f"SELECT * FROM Student WHERE {keys[0]} <> '{values}'")
                    
    #         elif keys[1] == "in":
    #             sql_query = read_data(f"SELECT * FROM Student WHERE {keys[0]} in {tuple(values)}")
                
    #         elif keys[1] == "contains":
    #             sql_query = read_data(f"SELECT * FROM Student WHERE {keys[0]} like '%{values}%'")

    #     if len(sql_query) == 0:
    #         return []
    #     else:
    #         x = []
                
    #         for i in sql_query:
    #             ans = Student(i[1], i[2], i[3])
    #             ans.student_id = i[0]
    #             x.append(ans)
    #         return x
        
def write_data(sql_query):
	import sqlite3
	connection = sqlite3.connect("selected_students.sqlite3")
	#connection = sqlite3.connect("dbms/dbms_resources/students_db.sqlite3")
	crsr = connection.cursor() 
	crsr.execute("PRAGMA foreign_keys=on;") 
	crsr.execute(sql_query) 
	connection.commit() 
	connection.close()

def read_data(sql_query):
	import sqlite3
	connection = sqlite3.connect("selected_students.sqlite3")
	#connection = sqlite3.connect("dbms/dbms_resources/students_db.sqlite3")
	crsr = connection.cursor()
	crsr.execute(sql_query)
	ans= crsr.fetchall()
	connection.close()
	return ans
	
# selected_students = Student.filter(score__gt=89)
# print(selected_students)