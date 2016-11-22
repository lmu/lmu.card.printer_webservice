from datetime import date
from persistent import Persistent
from persistent.mapping import PersistentMapping
from pyramid_zodbconn import get_connection

import transaction


class ZODBRootFolder(PersistentMapping):
    def __init__(self):
        PersistentMapping.__init__(self)
        self.title = 'ZODB Root Folder'


class Root(ZODBRootFolder):
    __name__ = None
    __parent__ = None


class PersonFolder(PersistentMapping):
    def __init__(self):
        PersistentMapping.__init__(self)
        self.title = 'Person-Folder'


class CardFolder(PersistentMapping):
    def __init__(self):
        PersistentMapping.__init__(self)
        self.title = 'Person-Folder'


class PersonModel(Persistent):
    def __init__(self, person_id, name, born=date(year=1900, month=1, day=1)):
        Persistent.__init__(self)
        self.person_id = person_id
        self.name = name
        self.born = born


class CardModel(Persistent):
    def __init__(self, card_id, ub_id):
        Persistent.__init__(self)
        self.card_id = card_id
        self.ub_id = ub_id


def root_factory(request):
    conn = get_connection(request)
    zodb_root = conn.root()
    if 'app_root' not in zodb_root:
        zodb_root['root'] = Root()
    root = zodb_root['root']
    if 'person_root_folder' not in root:
        folder = PersonFolder()
        root['person_root_folder'] = folder
        transaction.commit()
    if 'card_root_folder' not in root:
        folder = CardFolder()
        root['card_root_folder'] = folder
        transaction.commit()
    return root
