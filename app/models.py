from app import db
from sqlalchemy.dialects.mysql import TINYINT, MEDIUMBLOB, INTEGER, BIGINT, SMALLINT

class flag_table(db.Model):
    __tablename__ = 'flag_table'
    flag_round = db.Column(INTEGER(11), primary_key=True)
    problem_id = db.Column(INTEGER(11), primary_key=True)
    flag_val = db.Column(db.VARCHAR(200))
    

    def __repr__(self):
        return '<flag_round: {0}, problem_id: {1}, flag_val: {2} >'.format(self.flag_round, self.problem_id, self.flag_val)



class flag_stolen(db.Model):
    __tablename__ = 'flag_stolen'
    problem_id = db.Column(INTEGER(11), primary_key=True)
    flag_stolen_id = db.Column(INTEGER(11), primary_key=True)
    ids = db.Column(db.BLOB)


    def __repr__(self):
        return '<ids: {0}, problem_id: {1} >'.format(self.ids, self.problem_id)



class problem(db.Model):
    __tablename__ = 'problem'
    problem_id = db.Column(INTEGER(11), primary_key=True)
    problem_name = db.Column(db.VARCHAR(100))

    def __repr__(self):
        return '<problem_id: {0}, problem_name: {1} >'.format(self.problem_id, self.problem_name)



class round_time(db.Model):
    __tablename__ = 'round_time'
    round_number = db.Column(INTEGER(11), primary_key=True)
    rount_start = db.Column(db.DATETIME)
    rount_end = db.Column(db.DATETIME)

    def __repr__(self):
        return '<round_number: {0}, rount_start: {1}, rount_end: {2} >'.format(self.round_number, self.rount_start, self.rount_end)





class raw_packet(db.Model):
    __tablename__ = 'raw_packet'
    packet_id = db.Column(BIGINT(20), primary_key=True)
    packet_time = db.Column(db.DATETIME)
    raw_pakcet_data = db.Column(MEDIUMBLOB)

    def __repr__(self):
        return '<packet_id: {0}, packet_time: {1}, raw_pakcet_data: {2} >'.format(self.packet_id, self.packet_time, self.raw_pakcet_data)


class ethernet_packet(db.Model):
    __tablename__ = 'ethernet_packet'
    packet_id = db.Column(BIGINT(20), primary_key=True)
    dst_mac_add = db.Column(db.BINARY(6))
    src_mac_add = db.Column(db.BINARY(6))
    ether_type = db.Column(SMALLINT(5))

    def __repr__(self):
        return '<packet_id: {0}, dst_mac_add: {1}, src_mac_add: {2}, ether_type: {3} >'.format(self.packet_id, self.dst_mac_add, self.src_mac_add, self.ether_type)


class tcp_ip_packet(db.Model):
    __tablename__ = 'tcp_ip_packet'
    packet_id = db.Column(BIGINT(20), primary_key=True)
    ip_header = db.Column(db.BINARY(60))
    tcp_header = db.Column(db.BINARY(60))
    src_ip = db.Column(db.BINARY(4))
    dst_ip = db.Column(db.BINARY(4))
    src_port = db.Column(SMALLINT(6))
    dst_port = db.Column(SMALLINT(6))
    payload_data = db.Column(MEDIUMBLOB)

    def __repr__(self):
        return '<packet_id: {0}, ip_header: {1}, tcp_header: {2}, src_ip: {3}, dst_ip: {4}, src_port: {5}, dst_port: {6}, payload_data: {7} >'.format(self.packet_id, self.ip_header, self.tcp_header, self.src_ip, self.dst_ip, self.src_port, self.dst_port, self.payload_data)


class udp_ip_packet(db.Model):
    __tablename__ = 'udp_ip_packet'
    packet_id = db.Column(BIGINT(20), primary_key=True)
    ip_header = db.Column(db.BINARY(60))
    src_ip = db.Column(db.BINARY(4))
    dst_ip = db.Column(db.BINARY(4))
    src_port = db.Column(SMALLINT(5))
    dst_port = db.Column(SMALLINT(5))
    payload_data = db.Column(MEDIUMBLOB)

    def __repr__(self):
        return '<packet_id: {0}, ip_header: {1}, src_ip: {2}, dst_ip: {3}, src_port: {4}, dst_port: {5}, payload_data: {6} >'.format(self.packet_id, self.ip_header, self.src_ip, self.dst_ip, self.src_port, self.dst_port, self.payload_data)
