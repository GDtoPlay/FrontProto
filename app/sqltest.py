import unittest
import dbconnect

class MYSQLTest(unittest,TestCase):

    def test_ethernet_packet(self):
        sql= 'select problem_name from problem where problem_id = 1'
        result= 'test'
        c=db.engine.execute(sql)
        print(c)
        self.assertEqual(c,result)

#    def test_flag_stolen(unittest.TestCase):
#        sql= 'select 
#        result=
#        c=db.engine.execute(sql)
#        self.assertEqual(c,result)

    
