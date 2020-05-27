def read_data(sql_query):
    import sqlite3
    connection = sqlite3.connect("students.sqlite3")
    crsr = connection.cursor() 
    crsr.execute(sql_query) 
    ans= crsr.fetchall()  
    connection.close() 
    return ans

class InvalidField(Exception):
    pass

class Student:
    def __init__(self,name=None,age=None,score=None):
        self.name=name
        self.age=age
        self.student_id=None
        self.score=score  
        
    @staticmethod
    def filter(**kwargs):
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
            sql_query = " " + mul_conditions
        return sql_query
    
    @classmethod
    def aggregate(cls, aggregation,field=None, **kwargs):
        if len(kwargs) >= 1:
            sql_query = f"select {aggregation}({field}) from student where {Student.filter(**kwargs)}"
        elif field == None:
            sql_query = "select count(*) from student"
            
        else:
            if field not in ('name', 'age', 'score', 'student_id'):
                raise InvalidField
            else:
                sql_query = f"select {aggregation}({field}) from student"
        
        ans = read_data(sql_query)
        return ans[0][0]
    
    @classmethod
    def avg(cls, field, **kwargs):
        ans = cls.aggregate('avg', field, **kwargs)
        return ans
    
    @classmethod
    def min(cls,field, **kwargs):
        ans = cls.aggregate('min', field, **kwargs)
        return ans
    
    @classmethod
    def max(cls, field, **kwargs):
        ans = cls.aggregate('max', field, **kwargs)
        return  ans
    
    @classmethod
    def sum(cls, field, **kwargs):
        ans = cls.aggregate('sum', field, **kwargs)
        return ans
    
    @classmethod
    def count(cls,field=None, **kwargs):
        ans = cls.aggregate('count', field, **kwargs)
        return ans

    # @classmethod
    # def aggregate(cls, aggregation,field=None, **kwargs):
    #     if field not in ('name', 'age', 'score', 'student_id'):
    #         raise InvalidField
    #     if len(kwargs) >= 1:
    #         sql_query = f"select {aggregation}({field}) from student where {Student.filter(**kwargs)}"
    #     elif field == None:
    #         sql_query = "select count(*) from student"
            
    #     else:
    #         sql_query = f"select {aggregation}({field}) from student"
        
    #     ans = read_data(sql_query)
    #     return ans[0][0]

    # @classmethod
    # def avg(cls, field, **kwargs):
    #     if field not in ('name', 'age', 'score', 'student_id'):
    #             raise InvalidField
    #     if len(kwargs) >= 1:
    #         sql_query = f"select avg({field}) from student where {Student.filter(**kwargs)}"
    #     else:
    #         sql_query = f"select avg({field}) from student"
    
    #     ans = read_data(sql_query)
    #     return ans[0][0]
    
    # @classmethod
    # def min(cls, field, **kwargs):
    #     if field not in ('name', 'age', 'score', 'student_id'):
    #             raise InvalidField
    #     if len(kwargs) >= 1:
    #         sql_query = f"select min({field}) from student where {Student.filter(**kwargs)}"
    #     else:
    #         sql_query = f"select min({field}) from student"
    
    #     ans = read_data(sql_query)
    #     return ans[0][0]
    
    # @classmethod
    # def max(cls, field, **kwargs):
    #     if field not in ('name', 'age', 'score', 'student_id'):
    #             raise InvalidField
    #     if len(kwargs) >= 1:
    #         sql_query = f"select max({field}) from student where {Student.filter(**kwargs)}"
    #     else:
    #         sql_query = f"select max({field}) from student"
    
    #     ans = read_data(sql_query)
    #     return ans[0][0]
        
    # @classmethod
    # def sum(cls, field, **kwargs):
    #     if field not in ('name', 'age', 'score', 'student_id'):
    #             raise InvalidField
    #     if len(kwargs) >= 1:
    #         sql_query = f"select sum({field}) from student where {Student.filter(**kwargs)}"
    #     else:
    #         sql_query = f"select sum({field}) from student"
    
    #     ans = read_data(sql_query)
    #     return ans[0][0]
        
    # @classmethod
    # def count(cls, field = None, **kwargs):
    #     if field == None:
    #         sql_query = "select count(*) from student"    
        
    #     elif field not in ('name','age','score','student_id'):
    #             raise InvalidField
                
    #     elif len(kwargs)>=1:
    #         sql_query = f"select count({field}) from student where {Student.filter(**kwargs)}"
    #     else:
    #         sql_query = f"select count({field}) from student"        
    
    #     ans=read_data(sql_query)
    #     return ans[0][0]





    # @classmethod
    # def aggregate(cls,aggregation,field=None,**kwargs):
    #     fields=["name","student_id","age","score"]
    #     if(len(kwargs)>=1):
    #         query_att_string=cls.filter(**kwargs)
    #         multiple_sql_query="select {}({}) from student where {}".format(aggregation,field,query_att_string)
    #     elif(field==None):
    #         multiple_sql_query="select count(*) from student"
    #     else:
    #         if(field not in fields):
    #             raise InvalidField
    #         else:
    #             multiple_sql_query="select {}({}) from student".format(aggregation,field) 
    #     ans=read_data(multiple_sql_query)
    #     ans=ans[0][0]
    #     return ans
        
    # @classmethod
    # def avg(cls,field,**kwargs):
    #     ans=cls.aggregate("avg",field,**kwargs)
    #     return ans
    
    # @classmethod
    # def min(cls,field,**kwargs):
    #     ans=cls.aggregate("min",field,**kwargs)
    #     return ans
    
    # @classmethod
    # def max(cls, field, **kwargs):
    #     ans=cls.aggregate("max",field,**kwargs)
    #     return ans
    
    # @classmethod
    # def sum(cls, field, **kwargs):
    #     ans=cls.aggregate("sum",field,**kwargs)
    #     return ans
    
    # @classmethod
    # def count(cls, field=None, **kwargs):
    #     ans=cls.aggregate("count",field,**kwargs)
    #     return ans