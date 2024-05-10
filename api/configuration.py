import config
from recognition.Recognition import Recognition


recognition = Recognition()


def get_configuration(request):
    return {
        'video_source': config.video_source,
        'tolerance': config.tolerance,
        'active_rate': config.active_rate,
    }


def update_configuration(request):
    video_source = request.json.get('video_source')
    tolerance = request.json.get('tolerance')

    error = recognition.configure(
        video_source=video_source, tolerance=tolerance)

    if error:
        raise Exception(error)

    config.video_source = video_source
    config.tolerance = tolerance

    return get_configuration(request)
