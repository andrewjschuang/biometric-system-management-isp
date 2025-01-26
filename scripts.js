db.members.find(
  {
      "calendar.2024-08-11": { $ne: false }
  },
  {
      "name": 1,
      _id: 0
  }
)


db.events.find(
  {},
  {
    "name": 1,
    "face_distance": 1,
    _id: 0
  }
)


// mongo migrate calendar
db.members.find().forEach(function (member) {
  const newCalendar = Object.keys(member.calendar || {})
    .filter((date) => member.calendar[date] === true)
    .sort();

  db.members.updateOne(
    { _id: member._id },
    { $set: { calendar: newCalendar } }
  );
});
