from pymongo import MongoClient

class Veetreen(object):

    def __init__(self, name=None,alias=None,propietary_google_id=None, domain=None):
        self.name = name
        self.alias = alias
        self.propietary_google_id = propietary_google_id
        self.domain = domain

        self.client, self.database = self._init_db()

    @staticmethod
    def _init_db():
        client = MongoClient()
        database = client.veetreen
        return client, database

    @staticmethod
    def get_all():
        _ , database = Veetreen._init_db()
        rows = database.veetreens.find()
        models = []
        for row in rows:
            models.append(
                Veetreen(
                    name=row["name"],
                    alias=row["alias"],
                    propietary_google_id=row["propietary_google_id"],
                    domain=row["domain"]
                )
            )
        return models

    def update(self):
        pass

    def create(self):
        new_veetreen = {
            "name": self.name,
            "alias": self.alias,
            "propietary_google_id": self.propietary_google_id,
            "domain": self.domain
        }

        self.database.veetreens.insert_one(new_veetreen)

    def delete(self):
        pass

    def __str__(self):
        return str({
            "name": self.name,
            "alias": self.alias,
            "propietary_google_id": self.propietary_google_id,
            "domain": self.domain
        })


if __name__ == "__main__":

    col = Veetreen.get_all()

    for row in col:
        print(row)
