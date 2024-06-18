from recognition.Recognition import Recognition


recognition = Recognition()


def get_events(request):
    start_range = request.args.get('start_range', type=int)
    end_range = request.args.get('end_range', type=int)
    confirmed = request.args.get('confirmed')
    events = recognition.events_db.get_events_by_date(
        start_range, end_range, confirmed)
    return [x.to_dict() for x in events]
