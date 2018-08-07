#script for forms.py

#script for routes.py
@app.route('/tcpAndUdpSearch', methods=['GET'])
def tcpAndUdpSearch():
    page = request.args.get('page', default = 1, type = int)
    sql = 'select packet_id from raw_packet Limit '
    packet_ids = db.engine.execute(sql + str(10*(int(page) - 1)) + ', 10')
    TcpList = []
    UdpList = []
    for pack_id in packet_ids:    #type 0 : TCP,  1 : UDP
        tsql = 'select * from tcp_ip_packet where packet_id = '
        tcp_pack = db.engine.execute(tsql + str(pack_id.packet_id))
        if tcp_pack.rowcount is 0:
            usql = 'select * from udp_ip_packet where packet_id = '
            udp_pack = db.engine.execute(usql + str(pack_id.packet_id))
            for UDP in udp_pack:
            
                # src_ip str
                src_ipInt = ''
                for ToHex in UDP.src_ip:
                    src_ipInt = src_ipInt + str(ord(ToHex)) + '.'
                src_ipInt = src_ipInt[:-1]

                # dst_ip str
                dst_ipInt = ''
                for ToHex in UDP.dst_ip:
                    dst_ipInt = src_ipInt + str(ord(ToHex)) + '.'
                dst_ipInt = dst_ipInt[:-1]

                # payload_data hex
                hex_str = ''
                for ToHex in UDP.payload_data:
                    hex_str = hex_str + hex(ord(ToHex)) + ' '
                hex_str = hex_str[:-1]

                UdpList.append([1, UDP, src_ipInt, dst_ipInt, hex_str])
        else:
            for TCP in tcp_pack:

                # src_ip str
                src_ipInt = ''
                for ToHex in TCP.src_ip:
                    src_ipInt = src_ipInt + str(ord(ToHex)) + '.'
                src_ipInt = src_ipInt[:-1]

                # dst_ip str
                dst_ipInt = ''
                for ToHex in TCP.dst_ip:
                    dst_ipInt = src_ipInt + str(ord(ToHex)) + '.'
                dst_ipInt = dst_ipInt[:-1]

                # payload_data hex
                hex_str = ''
                for ToHex in TCP.payload_data:
                    hex_str = hex_str + hex(ord(ToHex)) + ' '
                hex_str = hex_str[:-1]

                TcpList.append([0, TCP, src_ipInt, dst_ipInt, hex_str])

    return render_template('tcpAndUdpSearch.html', title='tcpAndUdpSearch', TcpList=TcpList, UdpList=UdpList, page=page)
