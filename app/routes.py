import os
from flask import render_template, request, redirect, url_for, flash
from app import app, ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from app import app, db
from app.forms import *
from app.models import *
from app.parser import parser
from werkzeug import secure_filename
from datetime import datetime
from DatetimeCalc import InFiveMin
from binToAsc import binToAsc
from IpParser import IpParser

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/inputKeys', methods=['GET', 'POST'])
def inputKeys():
    form = RegistrationForm()
    if form.validate_on_submit():
        key = flag_table(flag_val=form.flag_val.data, flag_round=form.flag_round.data, problem_id=form.problem_id.data)
        db.session.add(key)
        db.session.commit()
        flash('Key has submitted')
        return redirect(url_for('index'))
    return render_template('inputKeys.html', title='inputKeys', form=form)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploadTest', methods=['GET', 'POST'])
def uploadTest():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template('uploadTest.html', title='uploadTest')


@app.route('/inputProb', methods=['GET', 'POST'])
def inputProb():
    form = ProbInsertForm()
    if form.validate_on_submit():
        Prob = problem(problem_id=form.problem_id.data, problem_name=form.problem_name.data)
        db.session.add(Prob)
        db.session.commit()
        flash('Prob has submitted')
        return redirect(url_for('index'))
    return render_template('inputProb.html', title='inputProb', form=form)



@app.route('/deleteProb', methods=['GET', 'POST'])
def deleteProb():
    form = ProbDeleteForm()
    if form.validate_on_submit():
        Del = problem.query.filter_by(problem_id=form.problem_id.data).first()
        db.session.delete(Del)
        db.session.commit()
        flash('Prob has deleted')
        return redirect(url_for('index'))
    return render_template('deleteProb.html', title='deleteProb', form=form)

@app.route('/listProb', methods=['GET', 'POST'])
def listProb():
    form = ProbListForm()
    if form.validate_on_submit():
        Select = problem.query.filter_by(problem_id=form.problem_id.data).first()
        return render_template('listProb.html', title='listProb', form=form, List=[], Select=Select)
    List = db.engine.execute('select * from problem')
    return render_template('listProb.html', title='listProb', form=form, List=List, Select=None)


@app.route('/inputRounds', methods=['GET', 'POST'])
def inputRounds():
    form = RoundInsertForm()
    if form.validate_on_submit():
        if form.rount_start.data >= form.rount_end.data:
            flash('Invalid round_start, round_end')
            return redirect(url_for('inputRounds'))
        Round = round_time(round_number=form.round_number.data, rount_start=form.rount_start.data, rount_end=form.rount_end.data)
        db.session.add(Round)
        db.session.commit()
        flash('Round has submitted')
        return redirect(url_for('index'))
    return render_template('inputRound.html', title='inputRound', form=form)


@app.route('/deleteRound', methods=['GET', 'POST'])
def deleteRound():
    form = RoundDeleteForm()
    if form.validate_on_submit():
        Del = round_time.query.filter_by(round_number=form.round_number.data).first()
        db.session.delete(Del)
        db.session.commit()
        flash('Round has deleted')
        return redirect(url_for('index'))
    return render_template('deleteRound.html', title='deleteRound', form=form)


@app.route('/listRound', methods=['GET', 'POST'])
def listRound():
    form = RoundListForm()
    if form.validate_on_submit():
        Select = db.engine.execute('select * from round_time where round_number = ' + str(form.round_number.data))
        return render_template('listRound.html', title='listRound', form=form, List=[], Select=Select)
    List = db.engine.execute('select * from round_time')
    return render_template('listRound.html', title='listRound', form=form, List=List, Select=None)


# for test not a real function to be served
@app.route('/inputFlagStolen', methods=['GET', 'POST'])
def inputFlagStolen():
    form = FlagStolenInsertForm()
    if form.validate_on_submit():
        FlagStolen = flag_stolen(problem_id=form.problem_id.data, flag_stolen_id=form.flag_stolen_id.data, ids=form.ids.data)
        db.session.add(FlagStolen)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('inputFlagStolen.html', title='inputFlagStolen', form=form)


# for test not a real function to be served
@app.route('/deleteFlagStolen', methods=['GET', 'POST'])
def deleteFlagStolen():
    form = FlagStolenDeleteForm()
    if form.validate_on_submit():
        Del = flag_stolen.query.filter_by(problem_id=form.problem_id.data).first()
        db.session.delete(Del)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('deleteFlagStolen.html', title='deleteFlagStolen', form=form)


@app.route('/listFlagStolen', methods=['GET', 'POST'])
def listFlagStolen():
    form = FlagStolenListForm()
    view_list = []
    butten = None
    sql = 'select * from flag_stolen where problem_id = '
    if form.validate_on_submit():
        Prob = problem.query.filter_by(problem_id=form.problem_id.data).first()
        butten = db.engine.execute(sql + str(Prob.problem_id))
        view_list.append([Prob.problem_id, butten])
        return render_template('listFlagStolen.html', title='listFlagStolen', form=form, view_list=view_list)
    prob_list = db.engine.execute('select problem_id from problem')
    for prob in prob_list:
        butten = None
        butten = db.engine.execute(sql + str(prob.problem_id))
        view_list.append([prob.problem_id, butten])
    return render_template('listFlagStolen.html', title='listFlagStolen', form=form, view_list=view_list)


@app.route('/stolenFlag', methods=['GET'])
def stolenFlag():
    problem_id = request.args.get('problem_id')
    sql = 'select * from flag_stolen where problem_id = '
    stolen_list = db.engine.execute(sql + str(problem_id))
    hex_list = []
    Nstolen_list = []
    for stolen in stolen_list:
        prob_id = stolen.problem_id
        validity = stolen.validity
        hex_str = ''
        for ToHex in stolen.ids:
            hex_str = hex_str + hex(ord(ToHex)) + ' '
        hex_str = hex_str[:-1]
        Nstolen_list.append([prob_id, hex_str, validity])
    return render_template('StolenFlag.html', title='stolenFlag', Nstolen_list=Nstolen_list)


@app.route('/stealingPacket', methods=['POST'])
def stealingPacket():
    packets = request.form['packets']
    parsed_packets = parser(packets)
    return render_template('StealingPacket.html', title='stealingPacket', parsed_packets=parsed_packets)


@app.route('/searchByVali', methods=['GET'])
def searchByVali():
    validity = request.args.get('validity')
    sql = 'select * from flag_stolen where validity = '
    stolen_list = db.engine.execute(sql + str(validity))
    hex_list = []
    Nstolen_list = []
    for stolen in stolen_list:
        prob_id = stolen.problem_id
        validity = stolen.validity
        hex_str = ''
        for ToHex in stolen.ids:
            hex_str = hex_str + hex(ord(ToHex)) + ' '
        hex_str = hex_str[:-1]
        Nstolen_list.append([prob_id, hex_str, validity])
    return render_template('searchByVali.html', title='searchByVali', Nstolen_list=Nstolen_list)


@app.route('/datetimeSearch', methods=['GET', 'POST'])
def datetimeSearch():
    form = DatetimeSearchForm()
    return render_template('datetimeSearch.html', title='datetimeSearch', form=form)


@app.route('/showDatetimeSearch', methods=['GET', 'POST'])
def showDatetimeSearch():
    form = DatetimeSearchForm(request.form)
    page = request.form['page']
    
    #page set
    if int(page) > 1:
        BackPage = int(page) - 1
    else:
        BackPage = int(page)
    FrontPage = int(page) + 1

    #datetime Day and Time
    time_start = str(form.time_start.data)

    time_end = str(form.time_end.data)


    if not InFiveMin(form.time_start.data, form.time_end.data):
        flash('time interval is more then 5 min')
        return redirect(url_for('datetimeSearch'))
    sql = 'select * from raw_packet where packet_time BETWEEN '
    Show = db.engine.execute(sql + "'" + str(form.time_start.data) + "'" + ' AND ' + "'" + str(form.time_end.data) + "'" + 'Limit ' + str(10*(int(page) - 1)) + ', 10')
    Nshow_list = []
    for raw_pac in Show:

        hex_str = ''
        for ToHex in raw_pac.raw_packet_data:
            hex_str = hex_str + hex(ord(ToHex)) + ' '
        hex_str = hex_str[:-1]

        # payload_data ascii
        asc_str = ''
        asc_str = binToAsc(raw_pac.raw_packet_data)

        Nshow_list.append([raw_pac, hex_str, asc_str])
    return render_template('showDatetimeSearch.html', title='showDatetimeSearch', Nshow_list=Nshow_list, time_start=time_start, time_end=time_end, BackPage=BackPage, FrontPage=FrontPage, form=form)


@app.route('/datetimeSearchDif', methods=['GET', 'POST'])
def datetimeSearchDif():
    form = DatetimeSearchForm()
    return render_template('datetimeSearchDif.html', title='datetimeSearchDif', form=form)


@app.route('/showDatetimeSearchDif', methods=['GET', 'POST'])
def showDatetimeSearchDif():
    form = DatetimeSearchForm(request.form)
    page = request.form['page']
    
    #page set
    if int(page) > 1:
        BackPage = int(page) - 1
    else:
        BackPage = int(page)
    FrontPage = int(page) + 1

    #datetime Day and Time
    time_start = str(form.time_start.data)

    time_end = str(form.time_end.data)


    if not InFiveMin(form.time_start.data, form.time_end.data):
        flash('time interval is more then 5 min')
        return redirect(url_for('datetimeSearch'))
    sql = 'select packet_id from raw_packet where packet_time BETWEEN '

    Show = db.engine.execute(sql + "'" + str(form.time_start.data) + "'" + ' AND ' + "'" + str(form.time_end.data) + "'" + 'Limit ' + str(10*(int(page) - 1)) + ', 10')
    TcpList = []
    UdpList = []
    for pack_id in Show:
        tsql = 'select * from tcp_ip_packet where packet_id = '
        tcp_pack = db.engine.execute(tsql + str(pack_id.packet_id))
        if tcp_pack.rowcount < 1:
            usql = 'select * from udp_ip_packet where packet_id = '
            udp_pack = db.engine.execute(usql + str(pack_id.packet_id))

            for UDP in udp_pack:
                # ip_header hex
                ip_headerInt = ''
                for ToHex in UDP.ip_header:
                    ip_headerInt = ip_headerInt + hex(ord(ToHex)) + ' '
                ip_headerInt = ip_headerInt[:-1]

                # src_ip str
                src_ipInt = ''
                for ToHex in UDP.src_ip:
                    src_ipInt = src_ipInt + str(ord(ToHex)) + '.'
                src_ipInt = src_ipInt[:-1]

                # dst_ip str
                dst_ipInt = ''
                for ToHex in UDP.dst_ip:
                    dst_ipInt = dst_ipInt + str(ord(ToHex)) + '.'
                dst_ipInt = dst_ipInt[:-1]

                # payload_data hex
                hex_str = ''
                for ToHex in UDP.payload_data:
                    hex_str = hex_str + hex(ord(ToHex)) + ' '
                hex_str = hex_str[:-1]

                # payload_data ascii
                asc_str = ''
                asc_str = binToAsc(UDP.payload_data)

                UdpList.append([1, UDP, src_ipInt, dst_ipInt, hex_str, asc_str, ip_headerInt])
        else:
            for TCP in tcp_pack:
                # tcp_header hex

                tcp_headerInt = ''
                for ToHex in TCP.tcp_header:
                    tcp_headerInt = tcp_headerInt + hex(ord(ToHex)) + ' '
                tcp_headerInt = tcp_headerInt[:-1]

                # ip_header hex
                ip_headerInt = ''
                for ToHex in TCP.ip_header:
                    ip_headerInt = ip_headerInt + hex(ord(ToHex)) + ' '
                ip_headerInt = ip_headerInt[:-1]

                # src_ip str
                src_ipInt = ''
                for ToHex in TCP.src_ip:

                    src_ipInt = src_ipInt + str(ord(ToHex)) + '.'
                src_ipInt = src_ipInt[:-1]

                # dst_ip str
                dst_ipInt = ''
                for ToHex in TCP.dst_ip:
                    dst_ipInt = dst_ipInt + str(ord(ToHex)) + '.'
                dst_ipInt = dst_ipInt[:-1]

                # payload_data hex
                hex_str = ''
                for ToHex in TCP.payload_data:
                    hex_str = hex_str + hex(ord(ToHex)) + ' '
                hex_str = hex_str[:-1]

                # payload_data ascii
                asc_str = ''
                asc_str = binToAsc(TCP.payload_data)

                TcpList.append([0, TCP, src_ipInt, dst_ipInt, hex_str, asc_str, ip_headerInt, tcp_headerInt])

        
    return render_template('showDatetimeSearchDif.html', title='showDatetimeSearchDif', TcpList=TcpList, UdpList=UdpList, time_start=time_start, time_end=time_end, BackPage=BackPage, FrontPage=FrontPage, form=form)


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
        if tcp_pack.rowcount < 1:
            usql = 'select * from udp_ip_packet where packet_id = '
            udp_pack = db.engine.execute(usql + str(pack_id.packet_id))
            for UDP in udp_pack:
                # ip_header hex
                ip_headerInt = ''
                for ToHex in UDP.ip_header:
                    ip_headerInt = ip_headerInt + hex(ord(ToHex)) + ' '
                ip_headerInt = ip_headerInt[:-1]

                # src_ip str
                src_ipInt = ''
                for ToHex in UDP.src_ip:
                    src_ipInt = src_ipInt + str(ord(ToHex)) + '.'
                src_ipInt = src_ipInt[:-1]

                # dst_ip str
                dst_ipInt = ''
                for ToHex in UDP.dst_ip:
                    dst_ipInt = dst_ipInt + str(ord(ToHex)) + '.'
                dst_ipInt = dst_ipInt[:-1]

                # payload_data hex
                hex_str = ''
                for ToHex in UDP.payload_data:
                    hex_str = hex_str + hex(ord(ToHex)) + ' '
                hex_str = hex_str[:-1]

                # payload_data ascii
                asc_str = ''
                asc_str = binToAsc(UDP.payload_data)

                UdpList.append([1, UDP, src_ipInt, dst_ipInt, hex_str, asc_str, ip_headerInt])
        else:
            for TCP in tcp_pack:
                # tcp_header hex
                tcp_headerInt = ''
                for ToHex in TCP.tcp_header:
                    tcp_headerInt = tcp_headerInt + hex(ord(ToHex)) + ' '
                tcp_headerInt = tcp_headerInt[:-1]

                # ip_header hex
                ip_headerInt = ''
                for ToHex in TCP.ip_header:
                    ip_headerInt = ip_headerInt + hex(ord(ToHex)) + ' '
                ip_headerInt = ip_headerInt[:-1]

                # src_ip str
                src_ipInt = ''
                for ToHex in TCP.src_ip:
                    src_ipInt = src_ipInt + str(ord(ToHex)) + '.'
                src_ipInt = src_ipInt[:-1]

                # dst_ip str
                dst_ipInt = ''
                for ToHex in TCP.dst_ip:
                    dst_ipInt = dst_ipInt + str(ord(ToHex)) + '.'
                dst_ipInt = dst_ipInt[:-1]

                # payload_data hex
                hex_str = ''
                for ToHex in TCP.payload_data:
                    hex_str = hex_str + hex(ord(ToHex)) + ' '
                hex_str = hex_str[:-1]

                # payload_data ascii
                asc_str = ''
                asc_str = binToAsc(TCP.payload_data)

                TcpList.append([0, TCP, src_ipInt, dst_ipInt, hex_str, asc_str, ip_headerInt, tcp_headerInt])

    return render_template('tcpAndUdpSearch.html', title='tcpAndUdpSearch', TcpList=TcpList, UdpList=UdpList, page=page)


@app.route('/dstIpSearchInput', methods=['GET', 'POST'])
def dstIpSearchInput():
    form = DstIpSearchForm()
    return render_template('dstIpSearchInput.html', title='dstIpSearchInput', form=form)

@app.route('/dstIpSearch', methods=['GET', 'POST'])
def dstIpSearch():
    form = DstIpSearchForm(request.form)
    page = request.form['page']

    #for parameter
    dst_ip = str(form.dst_ip.data)

    dst_port = str(form.dst_port.data)

    TcpList = []
    UdpList = []

    #page set
    if int(page) > 1:
        BackPage = int(page) - 1
    else:
        BackPage = int(page)
    FrontPage = int(page) + 1
    
    tsql = 'select * from tcp_ip_packet where dst_ip = '
    tarIp = IpParser(form.dst_ip.data)

    if tarIp is -1:
        return redirect(url_for('dstIpSearchInput'))

    tsql = tsql + 'cast(' + str(tarIp)+ ' as binary(4)) and dst_port = ' + str(form.dst_port.data) +  ' Limit ' + str(10*(int(page) - 1)) + ', 10'
    tcp_pack = db.engine.execute(tsql)
        
    for foundTcp in tcp_pack:
        # tcp_header hex
        tcp_headerInt = ''
        for ToHex in foundTcp.tcp_header:
            tcp_headerInt = tcp_headerInt + hex(ord(ToHex)) + ' '
        tcp_headerInt = tcp_headerInt[:-1]

        # ip_header hex
        ip_headerInt = ''
        for ToHex in foundTcp.ip_header:
            ip_headerInt = ip_headerInt + hex(ord(ToHex)) + ' '
        ip_headerInt = ip_headerInt[:-1]

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

        TcpList.append([foundTcp, src_ipInt, dst_ipInt, hex_str, asc_str, ip_headerInt, tcp_headerInt])

    usql = 'select * from udp_ip_packet where dst_ip = '
    usql = usql + 'cast(' + str(tarIp)+ ' as binary(4)) and dst_port = ' + str(form.dst_port.data) +  ' Limit ' + str(10*(int(page) - 1)) + ', 10'
    udp_pack = db.engine.execute(usql)
        
    for foundUdp in udp_pack:
        # ip_header hex
        ip_headerInt = ''
        for ToHex in foundUdp.ip_header:
            ip_headerInt = ip_headerInt + hex(ord(ToHex)) + ' '
        ip_headerInt = ip_headerInt[:-1]

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

        UdpList.append([foundUdp, src_ipInt, dst_ipInt, hex_str, asc_str, ip_headerInt])
    return render_template('dstIpSearch.html', title='dstIpSearch', form=form, TcpList=TcpList, UdpList=UdpList, BackPage=BackPage, FrontPage=FrontPage, dst_ip=dst_ip, dst_port=dst_port)


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

    if tarIp is -1:
        return redirect(url_for('srcIpSearchInput'))

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
