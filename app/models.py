from app import db
from sqlalchemy.dialects.mysql import TINYINT

class flag_table(db.Model):
    __tablename__ = 'flag_table'
    flag_round = db.Column(db.Integer, db.ForeignKey('round_time.round_number'), primary_key=True)
    problem_id = db.Column(db.Integer, db.ForeignKey('problem.problem_id'), primary_key=True)
    flag_val = db.Column(db.VARCHAR(200), index = True, unique=True)
    

    def __repr__(self):
        return '<flag_round: {0}, problem_id: {1}, flag_val: {2} >'.format(self.flag_round, self.problem_id, self.flag_val)



class flag_stolen(db.Model):
    __tablename__ = 'flag_stolen'
    problem_id = db.Column(db.Integer, db.ForeignKey('problem.problem_id'), primary_key=True)
    ids = db.Column(db.VARCHAR(400))


    def __repr__(self):
        return '<ids: {0}, problem_id: {1} >'.format(self.ids, self.problem_id)



class problem(db.Model):
    __tablename__ = 'problem'
    problem_id = db.Column(db.Integer, primary_key=True)
    problem_name = db.Column(db.VARCHAR(100))

    def __repr__(self):
        return '<problem_id: {0}, problem_name: {1} >'.format(self.problem_id, self.problem_name)



class round_time(db.Model):
    __tablename__ = 'round_time'
    round_number = db.Column(db.Integer, primary_key=True)
    rount_start = db.Column(db.DATETIME)
    rount_end = db.Column(db.DATETIME)

    def __repr__(self):
        return '<round_number: {0}, rount_start: {1}, rount_end: {2} >'.format(self.round_number, self.rount_start, self.rount_end)





class raw_packet(db.Model):
    __tablename__ = 'raw_packet'
    packet_id = db.Column(db.BIGINT, primary_key=True)
    packet_time = db.Column(db.DATETIME)
    raw_pakcet_data = db.Column(db.VARCHAR(1536))

    def __repr__(self):
        return '<packet_id: {0}, packet_time: {1}, raw_pakcet_data: {2} >'.format(self.packet_id, self.packet_time, self.raw_pakcet_data)


class ethernet_packet(db.Model):
    __tablename__ = 'ethernet_packet'
    packet_id = db.Column(db.BIGINT, db.ForeignKey('raw_packet.packet_id'), primary_key=True)
    dst_mac_add = db.Column(db.CHAR(6))
    src_mac_add = db.Column(db.CHAR(6))
    ether_type = db.Column(db.SMALLINT)

    def __repr__(self):
        return '<packet_id: {0}, dst_mac_add: {1}, src_mac_add: {2}, ether_type: {3} >'.format(self.packet_id, self.dst_mac_add, self.src_mac_add, self.ether_type)


class tcp_ip_packet(db.Model):
    __tablename__ = 'tcp_ip_packet'
    packet_id = db.Column(db.BIGINT, db.ForeignKey('raw_packet.packet_id'), primary_key=True)
    ip_header = db.Column(db.VARCHAR(60))
    tcp_header = db.Column(db.VARCHAR(60))
    src_ip = db.Column(TINYINT(4))
    dst_ip = db.Column(TINYINT(4))
    src_port = db.Column(db.SMALLINT)
    dst_port = db.Column(db.SMALLINT)
    payload_data = db.Column(db.VARCHAR(1460))

    def __repr__(self):
        return '<packet_id: {0}, ip_header: {1}, tcp_header: {2}, src_ip: {3}, dst_ip: {4}, src_port: {5}, dst_port: {6}, payload_data: {7} >'.format(self.packet_id, self.ip_header, self.tcp_header, self.src_ip, self.dst_ip, self.src_port, self.dst_port, self.payload_data)


class udp_ip_packet(db.Model):
    __tablename__ = 'udp_ip_packet'
    packet_id = db.Column(db.BIGINT, db.ForeignKey('raw_packet.packet_id'), primary_key=True)
    ip_header = db.Column(db.VARCHAR(60))
    src_ip = db.Column(TINYINT(4))
    dst_ip = db.Column(TINYINT(4))
    src_port = db.Column(db.SMALLINT)
    dst_port = db.Column(db.SMALLINT)
    payload_data = db.Column(db.VARCHAR(1472))

    def __repr__(self):
        return '<packet_id: {0}, ip_header: {1}, src_ip: {2}, dst_ip: {3}, src_port: {4}, dst_port: {5}, payload_data: {6} >'.format(self.packet_id, self.ip_header, self.src_ip, self.dst_ip, self.src_port, self.dst_port, self.payload_data)
