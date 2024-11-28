from recognition.Recognition import Recognition


recognition = Recognition()


def get_configuration(request):
    return {
        'video_source': recognition.config_db.get_video_source(),
        'tolerance': recognition.config_db.get_tolerance(),
        'delay': recognition.config_db.get_delay(),
        'display_image': recognition.config_db.get_display_image(),
        'active_rate': recognition.config_db.get_active_rate(),
    }


def update_configuration(request):
    video_source = request.json.get('video_source')
    tolerance = request.json.get('tolerance')
    delay = request.json.get('delay')
    display_image = request.json.get('display_image')
    active_rate = request.json.get('active_rate')

    if video_source:
        recognition.config_db.set_video_source(video_source)
        recognition.update_video_source(video_source)

    if tolerance:
        try:
            tolerance = float(tolerance)
        except:
            raise Exception('Error: tolerance not a floating number')
        if tolerance < 0 or tolerance > 1:
            raise Exception('Error: tolerance not between 0 and 1')
        recognition.config_db.set_tolerance(tolerance)

    if delay:
        try:
            delay = float(delay)
        except:
            raise Exception('Error: delay not an integer')
        recognition.config_db.set_delay(delay)

    if display_image:
        if display_image.lower() == 'true' or display_image == '1':
            recognition.config_db.set_display_image(True)
        elif display_image.lower() == 'false' or display_image == '0':
            recognition.config_db.set_display_image(False)
        else:
            raise Exception('Error: config is not a valid value')

    if active_rate:
        try:
            float(active_rate)
        except:
            raise Exception('Error: active_rate not a floating number')
        recognition.config_db.set_active_rate(active_rate)

    return get_configuration(request)


def get_settings(request):
    return {
        "enable_match_confirmation": recognition.config_db.get_enable_match_confirmation(),
        "show_only_sundays": recognition.config_db.get_show_only_sundays()
    }


def update_settings(request):
    enable_match_confirmation = request.json.get('enable_match_confirmation')
    if enable_match_confirmation is not None:
        recognition.config_db.set_enable_match_confirmation(
            enable_match_confirmation)

    show_only_sundays = request.json.get('show_only_sundays')
    if show_only_sundays is not None:
        recognition.config_db.set_show_only_sundays(show_only_sundays)
