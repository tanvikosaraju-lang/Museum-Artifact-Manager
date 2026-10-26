class Artifact:
    def __init__(self, id, name, category, description, location_id, status):
        self.id = id
        self.name = name
        self.category = category
        self.description = description
        self.location_id = location_id
        self.status = status

class Location:
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

class PreservationRecord:
    def __init__(self, id, artifact_id, date, notes, conservator):
        self.id = id
        self.artifact_id = artifact_id
        self.date = date
        self.notes = notes
        self.conservator = conservator