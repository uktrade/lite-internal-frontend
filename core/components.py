from lite_forms.components import Custom


class PicklistPicker(Custom):
    def __init__(self, name, items):
        self.name = name
        super().__init__(template="components/picklist-picker.html",
                         data=items)
