import config
from recognition.Recognition import Recognition


recognition = Recognition()


def configure(request):
    if request.method == 'POST':
        video_source = request.form.get('video_source')
        tolerance = request.form.get('tolerance')
        active_rate = request.form.get('active_rate')

        error = recognition.configure(
            video_source=video_source, tolerance=tolerance)

        if error:
            raise Exception(error)

        config.video_source = video_source
        config.tolerance = tolerance
        config.active_rate = active_rate

    return {
        'video_source': config.video_source,
        'tolerance': config.tolerance,
        'active_rate': config.active_rate,
    }
