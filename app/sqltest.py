import unittest
import dbconnect
import os
import MySQLdb

class MYSQLTest(unittest.TestCase):

    def test_problem(self):
        sql= 'select problem_name from problem where problem_id = 1'
        result= 'test'
        c=dbconnect.db.engine.execute(sql)
        for row in c:
            print(row['problem_name'])
            self.assertEqual(row['problem_name'],result)


#    def test_flag_stolen(unittest.TestCase):
#        sql= 'select 
#        result=
#        c=db.engine.execute(sql)
#        self.assertEqual(c,result)

    

if __name__== '__main__':
    unittest.main()
