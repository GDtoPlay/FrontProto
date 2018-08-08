#script for forms.py
from IpParser import IpParser

class SrcIpSearchForm(FlaskForm):
    src_ip = StringField('src_ip', validators=[DataRequired()])
    src_port = IntegerField('src_port', validators=[DataRequired()])
    page = IntegerField('page', validators=[DataRequired()])
    submit = SubmitField('input Key')

    def validate_src_ip(self, src_ip):
        if IpParser(src_ip.data) is -1:
            raise ValidationError('Wrong input')

#script for routes.py
from IpParser import IpParser

@app.route('/srcIpSearchInput', methods=['GET', 'POST'])
def srcIpSearchInput():
    form = SrcIpSearchForm()
    return render_template('srcIpSearchInput.html', title='srcIpSearchInput', form=form)

@app.route('/srcIpSearch', methods=['GET', 'POST'])
def srcIpSearch():
    form = SrcIpSearchForm(request.form)
    page = request.form['page']

    #for parameter
    src_ip = str(form.src_ip.data)

    src_port = str(form.src_port.data)

    TcpList = []
    UdpList = []

    #page set
    if int(page) > 1:
        BackPage = int(page) - 1
    else:
        BackPage = int(page)
    FrontPage = int(page) + 1
    
    tsql = 'select * from tcp_ip_packet where src_ip = '
    tarIp = IpParser(form.src_ip.data)
    tsql = tsql + 'cast(' + str(tarIp)+ ' as binary(4)) and src_port = ' + str(form.src_port.data) +  ' Limit ' + str(10*(int(page) - 1)) + ', 10'
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
            dst_ipInt = dst_ipInt + str(ord(ToHex)) + '.'
        dst_ipInt = dst_ipInt[:-1]

        # payload_data hex
        hex_str = ''
        for ToHex in foundTcp.payload_data:
            hex_str = hex_str + hex(ord(ToHex)) + ' '
        hex_str = hex_str[:-1]

        # payload_data ascii
        asc_str = ''
        asc_str = binToAsc(foundTcp.payload_data)

        TcpList.append([foundTcp, src_ipInt, dst_ipInt, hex_str, asc_str])

    usql = 'select * from udp_ip_packet where src_ip = '
    usql = usql + 'cast(' + str(tarIp)+ ' as binary(4)) and src_port = ' + str(form.src_port.data) +  ' Limit ' + str(10*(int(page) - 1)) + ', 10'
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

        # payload_data ascii
        asc_str = ''
        asc_str = binToAsc(foundUdp.payload_data)

        UdpList.append([foundUdp, src_ipInt, dst_ipInt, hex_str, asc_str])
    return render_template('srcIpSearch.html', title='srcIpSearch', form=form, TcpList=TcpList, UdpList=UdpList, BackPage=BackPage, FrontPage=FrontPage, src_ip=src_ip, src_port=src_port)
