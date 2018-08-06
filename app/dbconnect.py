import os
import sqlalchemy
import MySQLdb

db=sqlalchemy.create_engine("mysql://root:1234@127.0.0.1:3306/ransomware")

import sqltest
