#script for forms.py

#script for routes.py
@app.route('/tcpAndUdpSearch', methods=['GET'])
def tcpAndUdpSearch():
    page = request.args.get('page')
    sql = 'select packet_id from raw_packet Limit'
    packet_ids = db.engine.execute(sql + str(10*(page - 1)) + ', 10')
    TcpAndUdp = []
    for pack_id in packet_ids:    #type 0 : TCP,  1 : UDP
        tsql = 'select * from tcp_ip_packet where packet_id = '
        tcp_pack = db.engine.execute(tsql + str(pack_id.packet_id))
        if tcp_pack is None:
            usql = 'select * from udp_ip_packet where packet_id = '
            udp_pack = db.engine.execute(usql + str(pack_id.packet_id))
            
            # src_ip str
            src_ipInt = ''
            for ToHex in udp_pack.src_ip:
                src_ipInt = src_ipInt + str(ord(ToHex)) + '.'
            src_ipInt = src_ipInt[:-1]

            # dst_ip str
            dst_ipInt = ''
            for ToHex in udp_pack.dst_ip:
                dst_ipInt = src_ipInt + str(ord(ToHex)) + '.'
            dst_ipInt = dst_ipInt[:-1]

            # payload_data hex
            hex_str = ''
            for ToHex in udp_pack.payload_data:
                hex_str = hex_str + hex(ord(ToHex)) + ' '
            hex_str = hex_str[:-1]

            TcpAndUdp.append([1, udp_pack, src_ipInt, dst_ipInt, hex_str])
        else:
            # src_ip str
            src_ipInt = ''
            for ToHex in udp_pack.src_ip:
                src_ipInt = src_ipInt + str(ord(ToHex)) + '.'
            src_ipInt = src_ipInt[:-1]

            # dst_ip str
            dst_ipInt = ''
            for ToHex in udp_pack.dst_ip:
                dst_ipInt = src_ipInt + str(ord(ToHex)) + '.'
            dst_ipInt = dst_ipInt[:-1]

            # payload_data hex
            hex_str = ''
            for ToHex in udp_pack.payload_data:
                hex_str = hex_str + hex(ord(ToHex)) + ' '
            hex_str = hex_str[:-1]

            TcpAndUdp.append([0, tcp_pack, src_ipInt, dst_ipInt, hex_str])


    render_template('tcpAndUdpSearch.html', title='tcpAndUdpSearch', TcpAndUdp=TcpAndUdp, page=page)
