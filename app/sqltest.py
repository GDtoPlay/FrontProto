import unittest
import dbconnect
import os
import MySQLdb
import datetime

class MYSQLTest(unittest.TestCase):

    def test_problem(self):
        sql= 'select problem_name from problem where problem_id = 1'
        result= 'test'
        c=dbconnect.db.engine.execute(sql)
        for row in c:
            print("\n"+str(row['problem_name']))
            self.assertEqual(row['problem_name'],result)


    def test_flag_stolen_search_with_ids(self):
        sql= 'select problem_id from flag_stolen where ids = 0x3E010000000000003F01000000000000400100000000000041010000000000004201000000000000430100000000000044010000000000004501000000000000'
        result= 0
        c=dbconnect.db.engine.execute(sql)
        for row in c:
            print("\n"+str(row['problem_id']))
            self.assertEqual(row['problem_id'],result)

    def test_flag_stolen_search_with_problem_id(self):
        sql = 'select ids from flag_stolen where problem_id = 0 and flag_stolen_id = 1'
        result = "3E010000000000003F01000000000000400100000000000041010000000000004201000000000000430100000000000044010000000000004501000000000000".decode("hex")
        c = dbconnect.db.engine.execute(sql)
        for row in c :
            d = row['ids']
            print("\n"+str(d))
            self.assertEqual(d,result)
    
    def test_flag_stolen_search_with_validity(self):
        sql = 'select ids from flag_stolen where validity = 3 and flag_stolen_id=1'
        result = "3F0000000000003F0000000000003F0000000000003F0000000000003F0000000000003F0000000000003F000000000000".decode("hex")
        c = dbconnect.db.engine.execute(sql)
        for row in c:
            num = 0
            d = row['ids']
            print("\n"+str(d))
            if num is 1:
                self.assertEqual(d,result)
            else:
                num=num+1

    def test_flag_table(self):
        sql = 'select flag_val from flag_table where problem_id = 0 and flag_round = 7'
        result = 'aa'
        c=dbconnect.db.engine.execute(sql)
        for row in c:
            d=row['flag_val']
            print("\n"+str(d))
            self.assertEqual(d,result)

    def test_round_time_start(self):
        sql = 'select * from round_time where round_number = 5'
        result = datetime.datetime(2016,9,2,0,25)
        c=dbconnect.db.engine.execute(sql)
        for row in c :
            d = row['round_start']
            print("\n"+str(d))
            self.assertEqual(d,result)

    def test_round_time_end(self):
        sql = 'select * from round_time where round_number = 5'
        result = datetime.datetime(2016,9,2,0,30)
        c=dbconnect.db.engine.execute(sql)
        for row in c :
            d = row['round_end']
            print("\n"+str(d))
            self.assertEqual(d,result)

    def test_raw_packet_search_time(self):
        sql = 'select packet_time from raw_packet where packet_id = 1'
        result = datetime.datetime(2016,9,2,19,33,3)
        c=dbconnect.db.engine.execute(sql)
        for row in c:
            d=row['packet_time']
            print("\n"+str(d))
            self.assertEqual(d,result)

    def test_raw_packet_search_data(self):
        sql = 'select raw_packet_data from raw_packet where packet_id = 1'
        result = "1AB7C96A3F00163E543F080045000044283F003F113F0A0301200A0509023F073F00301C050800000001000000010000001900015768617420646F20796F752077616E7420746F20646F3F203A".decode("hex")
        c=dbconnect.db.engine.execute(sql)
        for row in c:
            d=row['raw_packet_data']
            print("\n"+str(d))
            self.assertEqual(d,result)

    def test_udp_ip_packet_search_ip_header(self):
        sql = 'select * from udp_ip_packet where packet_id = 144'
        result = "450000683F40003F1168170A0301510A05080200".decode("hex")
        c=dbconnect.db.engine.execute(sql)
        for row in c:
            d=row['ip_header']
            print("\n"+str(d))
            self.assertEqual(d,result)

    def test_udp_ip_packet_search_src_ip(self):
        sql = 'select * from udp_ip_packet where packet_id = 144'
        result = "0A030151".decode("hex")
        c=dbconnect.db.engine.execute(sql)
        for row in c:
            d=row['src_ip']
            print("\n"+str(d))
            self.assertEqual(d,result)

    def test_udp_ip_packet_search_dst_ip(self):
        sql = 'select * from udp_ip_packet where packet_id = 144'
        result = "0A050802".decode("hex")
        c=dbconnect.db.engine.execute(sql)
        for row in c:
            d=row['dst_ip']
            print("\n"+str(d))
            self.assertEqual(d,result)

    def test_udp_ip_packet_search_src_port(self):
        sql = 'select * from udp_ip_packet where packet_id = 144'
        result = 46445
        c=dbconnect.db.engine.execute(sql)
        for row in c:
            d=row['src_port']
            print("\n"+str(d))
            self.assertEqual(d,result)

    def test_udp_ip_packet_search_dst_port(self):
        sql = 'select * from udp_ip_packet where packet_id = 144'
        result = 1999
        c=dbconnect.db.engine.execute(sql)
        for row in c:
            d=row['dst_port']
            print("\n"+str(d))
            self.assertEqual(d,result)

    def test_udp_ip_packet_search_payload_data(self):
        sql = 'select * from udp_ip_packet where packet_id = 144'
        result = "08000000B4AD0100070000003D0001546861742077616C6C20697320676F6E6E6120626520797575757575757575757575757575757575756765206B466F7052667353735541744C74766C0A".decode("hex")
        c=dbconnect.db.engine.execute(sql)
        for row in c:
            d=row['payload_data']
            print("\n"+str(d))
            self.assertEqual(d,result)
            
if __name__== '__main__':
    unittest.main()
