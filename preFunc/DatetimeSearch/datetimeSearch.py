from DatetimeCalc import InFiveMin

#script for forms.py
class DatetimeSearchForm(FlaskForm):
    time_start = DateTimeField('time_Start', format="%Y-%m-%d %H:%M:%S", validators=[DataRequired()])
    time_end = DateTimeField('time_End', format="%Y-%m-%d %H:%M:%S", validators=[DataRequired()])
    submit = SubmitField('input Key')

    def time_compair(self, time_start, time_end):
        if !InFiveMin(time_start, time_end):
            raise ValidationError('This problem_id does not exist')
#script for routes.py
@app.route('/datetimeSearch', methods=['GET', 'POST'])
def datetimeSearch():
    form = DatetimeSearchForm()
    if form.validate_on_submit():
	if !InFiveMin(form.time_start.data, form.time_end.data):
            flash('time interval is more then 5 min')
            return redirect(url_for('datetimeSearch'))
        sql = 'select * from raw_packet where DATE(packet_time) BETWEEN'
        Show = db.engine.execute(sql + str(form.time_start.data) + 'AND ' + str(form.time_end.data))
        Nshow_list = []
        for raw_pac in Show:
            hex_str = ''
            for ToHex in raw_pac.raw_pakcet_data:
                hex_str = hex_str + hex(ord(ToHex)) + ','
            hex_str = hex_str[:-1]
            Nshow_list.append([raw_pac, hex_str])
        render_template('showDatetimeSearch.html', title='showDatetimeSearch', Nshow_list=Nshow_list)
    return render_template('datetimeSearch.html', title='datetimeSearch', form=form)
