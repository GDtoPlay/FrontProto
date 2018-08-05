#script for forms.py
from IpParser import IpParser

class DstIpSearchForm(FlaskForm):
    dst_ip = StringField('dst_ip', validators=[DataRequired()])
    dst_port = IntegerField('dst_port', validators=[DataRequired()])
    submit = SubmitField('input Key')

    def validate_dst_ip(self, dst_ip):
        if IpParser(dst_ip.data) is -1:
            raise ValidationError('Wrong input')

#script for routes.py
from IpParser import IpParser

@app.route('/dstIpSearch', methods=['GET', 'POST'])
def dstIpSearch():
    form = DstIpSearchForm()
    TcpList = []
    UdpList = []
    if form.validate_on_submit():
        tsql = 'select * from tcp_ip_packet where dst_ip = '
        tarIp = IpParser(form.dst_ip.data)
        tsql = tsql + 'cast(' + str(hex(tarIp))+ ' as binary(4)) and dst_port = ' + str(form.dst_port.data)
        tcp_pack = db.engine.execute(tsql)
        
        for foundTcp in tcp_pack:
            # src_ip str
            src_ipInt = ''
            for ToHex in foundTcp.src_ip:
                src_ipInt = src_ipInt + str(ord(ToHex)) + '.'
            src_ipInt = src_ipInt[:-1]

            # dst_ip str
            dst_ipInt = ''
            for ToHex in foundTcp.dst_ip:
                dst_ipInt = src_ipInt + str(ord(ToHex)) + '.'
            dst_ipInt = dst_ipInt[:-1]

            # payload_data hex
            hex_str = ''
            for ToHex in foundTcp.payload_data:
                hex_str = hex_str + hex(ord(ToHex)) + ' '
            hex_str = hex_str[:-1]

            TcpList.append([foundTcp, src_ipInt, dst_ipInt, hex_str])

        usql = 'select * from udp_ip_packet where dst_ip = '
        usql = usql + 'cast(' + str(hex(tarIp))+ ' as binary(4)) and dst_port = ' + str(form.dst_port.data)
        udp_pack = db.engine.execute(usql)
        
        for foundUdp in udp_pack:
            # src_ip str
            src_ipInt = ''
            for ToHex in foundUdp.src_ip:
                src_ipInt = src_ipInt + str(ord(ToHex)) + '.'
            src_ipInt = src_ipInt[:-1]

            # dst_ip str
            dst_ipInt = ''
            for ToHex in foundUdp.dst_ip:
                dst_ipInt = src_ipInt + str(ord(ToHex)) + '.'
            dst_ipInt = dst_ipInt[:-1]

            # payload_data hex
            hex_str = ''
            for ToHex in foundUdp.payload_data:
                hex_str = hex_str + hex(ord(ToHex)) + ' '
            hex_str = hex_str[:-1]

            UdpList.append([foundUdp, src_ipInt, dst_ipInt, hex_str])
        return render_template('dstIpSearch.html', title='dstIpSearch', form=form, TcpList=TcpList, UdpList=UdpList)

    return render_template('dstIpSearch.html', title='dstIpSearch', form=form, TcpList=TcpList, UdpList=UdpList)
