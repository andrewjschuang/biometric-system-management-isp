from recognition.Recognition import Recognition


recognition = Recognition()


def phone_number_match(request):
    phone_number = request.form.get("phone_number")
    if (not phone_number):
        raise Exception('Error: missing phone_number')
    try:
        phone_number = int(phone_number)
    except:
        raise Exception('Error: invalid phone_number')

    event_name = request.form.get("event_name")
    if not event_name:
        raise Exception('Error: missing event_name')

    recognition.phone_number_match(phone_number, event_name)
