class Tab:
    def __init__(self, id, name, url, count=0):
        self.id = "tab-" + id
        self.name = name
        self.url = url
        self.count = count
