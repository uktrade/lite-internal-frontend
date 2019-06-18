class TeamsPages():

    def __init__(self, driver):
        self.driver = driver
        self.add_team_text_field = "name" #id

    def enter_team_name(self, text):
        return self.driver.find_element_by_id(text).send_keys(text)

