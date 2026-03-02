from recognition.Recognition import Recognition


recognition = Recognition()


def get_events(request):
    start_range = request.args.get('start_range', type=int)
    end_range = request.args.get('end_range', type=int)
    confirmed = request.args.get('confirmed')
    events = recognition.events_db.get_events_by_date(
        start_range, end_range, confirmed)

    members = recognition.members_db.get_all_members()
    member_names = {member.id: member.name for member in members}

    result = []
    for event in events:
        event_dict = event.to_dict()
        if event.member_id and event.member_id in member_names:
            event_dict['name'] = member_names[event.member_id]
        result.append(event_dict)

    return result
