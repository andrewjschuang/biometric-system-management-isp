import config
from recognition.Recognition import Recognition


recognition = Recognition()


def get_configuration(request):
    return {
        'video_source': config.video_source,
        'tolerance': config.tolerance,
        'delay': config.delay,
        'display_image': config.display_image,
    }


def update_configuration(request):
    video_source = request.json.get('video_source')
    tolerance = request.json.get('tolerance')
    delay = request.json.get('delay')
    display_image = request.json.get('display_image')

    if video_source:
        try:
            video_source = int(video_source)
        except:
            raise Exception('Error: video_source not an integer')
        config.video_source = video_source

    if tolerance:
        try:
            tolerance = float(tolerance)
        except:
            raise Exception('Error: tolerance not a floating number')
        if tolerance < 0 or tolerance > 1:
            raise Exception('Error: tolerance not between 0 and 1')
        config.tolerance = tolerance

    if delay:
        try:
            delay = float(delay)
        except:
            raise Exception('Error: delay not an integer')
        config.delay = delay

    if display_image:
        if display_image.lower() == 'true' or display_image == '1':
            config.display_image = True
        elif display_image.lower() == 'false' or display_image == '0':
            config.display_image = False
        else:
            raise Exception('Error: config is not a valid value')

    recognition.configure()

    return get_configuration(request)
