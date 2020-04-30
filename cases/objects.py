from munch import Munch


class Slice:
    def __init__(self, title, file):
        self.title = title
        self.file = file


class Case(Munch):
    @property
    def data(self):
        if "application" in self:
            return self["application"]
        else:
            return self["query"]

    @property
    def organisation(self):
        return self.data["organisation"]

    @property
    def status(self):
        return self.data["status"]["key"]

    @property
    def case_officer(self):
        return {}
        # return self.get("case_officer", {})
