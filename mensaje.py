class Mensaje(object):

    def __init__(self, id, datetime = None, text = None, id_parent = None):
        self.id = id
        self.datetime = None
        self.text = None
        self.id_parent = None

        if datetime is not None:
            self.datetime = datetime

        if text is not None:
            self.text = text

        if id_parent is not None:
            self.id_parent = id_parent


