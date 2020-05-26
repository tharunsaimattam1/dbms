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

    # @staticmethod
    # def filter(**kwargs):   
    #     li = []
    #     st = []
    #     for key, value in kwargs.items():
    #         keys = key
    #         #values = value
    #         field = keys.split('__')
    #         if field[0] not in ('student_id','name','age','score'):
    #             raise InvalidField
                
    #         if keys in  ('student_id','name','age','score'):
    #             if  key in ['student_id','age', 'score']:
    #                 q = 'SELECT * FROM Student WHERE {} = {}'.format(key,value)
    #                 query = read_data(q) 
            
    #             else:
    #                 q = 'SELECT * FROM Student WHERE {} = \'{}\' '.format(key,value)
    #                 query = read_data(q) 
            
    #             st.append(query)
            
    #         else:
    #             if field[1] == 'lt':
    #                 q = 'SELECT * FROM Student WHERE {} < {}'.format(field[0],value)
    #                 query = read_data(q) 
            
                
    #             if field[1] == 'gt':
    #                 q = 'SELECT * FROM Student WHERE {} > {}'.format(field[0],value)
    #                 query = read_data(q) 
            
                        
    #             if field[1] == 'lte':
    #                 q = 'SELECT * FROM Student WHERE {} <= {}'.format(field[0],value)
    #                 query = read_data(q) 
            
                        
    #             if field[1] == 'gte':
    #                 q = 'SELECT * FROM Student WHERE {} >= {}'.format(field[0],value)
    #                 query = read_data(q) 
            
                        
    #             if field[1] == 'neq':
    #                 if  field[0] in ['student_id','age', 'score']:
    #                     q = 'SELECT * FROM Student WHERE {} != {}'.format(field[0],value)
    #                     query = read_data(q) 
            
    #                 else:
    #                     q = 'SELECT * FROM Student WHERE {} != \'{}\' '.format(field[0],value)
    #                     query = read_data(q) 
            
                   
    #             if field[1] == 'in':
    #                 q = 'SELECT * FROM Student WHERE {} in {}'.format(field[0],tuple(value))
    #                 query = read_data(q) 
            
                        
    #             if field[1] == 'contains':
    #                 q = 'SELECT * FROM Student WHERE {} LIKE "%{}%" '.format(field[0],value)
    #                 query = read_data(q) 
            
            
    #             st.append(query)
    #         final = set.intersection(*[set(i) for i in st])
    #         final = sorted(final)
        
        
    #     if len(final) == 0:
    #         return []
            
    #     else:
    #         for i in range(len(final)):
    #             ans = Student(final[i][1],final[i][2],final[i][3])
    #             ans.student_id = final[i][0]
    #             li.append(ans)
    #         return li   

    @staticmethod
    def filter(**kwargs):
        objects_list=[]
        operator={'lt' : '<', 'lte' : '<=', 'gt' : '>', 'gte' : '>=', 'neq' : '!=', 'in' : 'in'}
        
        if(len(kwargs)) >= 1:
            conditions = []
            for key, value in kwargs.items():
                    
                    keys = key
                    keys = keys.split('__')
                    if keys[0] not in ('name', 'age', 'score', 'student_id'):
                            raise InvalidField 
            
                    if len(keys) == 1:
                        sql_query= f" {key} = '{value}'"
                    
                    elif keys[1] == 'in':
                        sql_query = f"{keys[0]} {operator[keys[1]]} {tuple(value)}"
                    
                    elif keys[1] == 'contains':
                        sql_query = f"{keys[0]} like '%{value}%'"
                    
                    else:    
                        sql_query = f"{keys[0]} {operator[keys[1]]} '{value}'"
                
                    conditions.append(sql_query)
                    
            mul_conditions = " and ".join(tuple(conditions))       
            sql_query = "select * from student where " + mul_conditions
            
        sql_query = read_data(sql_query)
        
        for i in sql_query:
            ans = Student(i[1], i[2], i[3])
            ans.student_id = i[0]
            objects_list.append(ans)
        return objects_list    




    # @staticmethod       
    # def filter(**kwargs):
    #     temp_list=[]
    #     final_list=[]
    #     iteration=1
    #     for key,value in kwargs.items():
    #         def key_fun(key):

    #             switcher={
    #                 'age': 'age={}'.format(value),
    #                 'age__lt': 'age < {}'.format(value),
    #                 'age__lte':'age <= {}'.format(value),
    #                 'age__gt': 'age > {}'.format(value),
    #                 'age__gte':'age >= {}'.format(value),
    #                 'age__neq': 'age <> {}'.format(value),
                    
    #                 'score': 'score={}'.format(value),
    #                 'score__lt': 'score < {}'.format(value),
    #                 'score__lte':'score <= {}'.format(value),
    #                 'score__gt': 'score > {}'.format(value),
    #                 'score__gte':'score >= {}'.format(value),
    #                 'score__neq': 'score <> {}'.format(value),
                    
    #                 'student_id': 'student_id={}'.format(value),
    #                 'student_id__lt': 'student_id < {}'.format(value),
    #                 'student_id__lte':'student_id <= {}'.format(value),
    #                 'student_id__gt': 'student_id > {}'.format(value),
    #                 'student_id__gte':'student_id >= {}'.format(value),
    #                 'student_id__neq': 'student_id <> {}'.format(value),
                    
    #                 'name': 'name=\'{}\''.format(value),
    #                 'name__neq': 'name <> \'{}\''.format(value),
    #                 'name__contains':'name like \'%{}\''.format(value)
    #             }
            
            
    #             condition=switcher.get(key)
    #             if(condition==None):
    #                 raise InvalidField
    #             query='SELECT * FROM Student WHERE {}'.format(condition)
    #             return query
            
    #         if key in['age__in','score__in','student_id__in','name__in']:
    #             value=tuple(value)
    #             query='SELECT * FROM Student WHERE {} in {}'.format(key[0:-4],value)
    #         else:
    #             query=key_fun(key)

    #         results=read_data(query)
    #         for i in results:
    #             if iteration==1:
    #                 temp_list.append(i)
    #             else:
    #                 temp_list=set(temp_list)
    #                 results=set(results)
    #                 temp_list=temp_list.intersection(results)

    #         iteration+=1
    #     for i in temp_list:
    #         student_obj=Student(i[1],i[2],i[3])
    #         student_obj.student_id=i[0]
    #         final_list.append(student_obj)
    #     return final_list


    # @classmethod    
    # def filter(cls, **kwargs):
    #     cls.li = []
    #     l  = []
    #     for key, value in kwargs.items():
    #         cls.keys = key
    #         cls.values = value
    #         keys = cls.keys
    #         x = keys.split("__")
        
    #         if x[0] not in ("student_id", "name", "age", "score"):
    #             raise InvalidField
                
    #         if len(x)>1:
    #             if x[1] == "lt":
    #                 sql_query = f"{x[0]} < {cls.values}"
                
    #             elif x[1] == "lte":
    #                 sql_query = f"{x[0]} <= {cls.values}"
                        
    #             elif x[1] == "gt":
    #                 sql_query = f"{x[0]} > {cls.values}"
                        
    #             elif x[1] == "gte":
    #                 sql_query = f"{x[0]} >= {cls.values}"
                        
    #             elif x[1] == "neq":
    #                 sql_query = f"{x[0]} <> '{cls.values}'"
                        
    #             elif x[1] == "in":
    #                 sql_query = f"{x[0]} in {tuple(cls.values)}"
                    
    #             elif x[1] == "contains":
    #                 sql_query = f"{x[0]} like '%{cls.values}%'"

    #         else:
    #             sql_query = f'{x[0]} = "{cls.values}"'
            
    #         l.append(sql_query)
            
    #         x = ' and '.join(tuple(l))
    #         x = 'SELECT * FROM Student WHERE '+x
            
    #         ans = read_data(x)
    #         for i in ans:
    #             an = Student(i[1], i[2], i[3])
    #             an.student_id = i[0]
    #             cls.li.append(an)
    #         return cls.li


def write_data(sql_query):
	import sqlite3
	#connection = sqlite3.connect("selected_students.sqlite3")
	connection = sqlite3.connect("dbms/dbms_resources/students_db.sqlite3")
	crsr = connection.cursor() 
	crsr.execute("PRAGMA foreign_keys=on;") 
	crsr.execute(sql_query) 
	connection.commit() 
	connection.close()

def read_data(sql_query):
	import sqlite3
	#connection = sqlite3.connect("selected_students.sqlite3")
	connection = sqlite3.connect("dbms/dbms_resources/students_db.sqlite3")
	crsr = connection.cursor()
	crsr.execute(sql_query)
	ans= crsr.fetchall()
	connection.close()
	return ans

ages = (25, 32)
selected_students = Student.filter(age__in=ages)
print(selected_students)