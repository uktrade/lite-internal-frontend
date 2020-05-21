from lite_forms.components import Option


class OpenGeneralExportLicences:
    class OpenGeneralLicence:
        def __init__(self, id, name, description, acronym):
            self.id = id
            self.name = name
            self.description = description
            self.acronym = acronym

    open_general_export_licence = OpenGeneralLicence(
        "00000000-0000-0000-0000-000000000002",
        "Open general export licence",
        "Licence which allows the export of specified controlled items by any exporter, removing the "
        "need for them to apply for an individual licence.",
        "OGEL",
    )
    open_general_trade_control_licence = OpenGeneralLicence(
        "00000000-0000-0000-0000-000000000013",
        "Open general trade control licence",
        "Licences which control the trafficking and brokering activity between one third country and "
        "another where the transaction or deal is brokered in the UK or by a UK person.",
        "OGTCL",
    )
    open_general_transhipment_licence = OpenGeneralLicence(
        "00000000-0000-0000-0000-000000000014",
        "Open general transhipment licence",
        "Transhipment licences allow controlled goods to pass through the UK on the way to other destinations.",
        "OGTL",
    )

    @classmethod
    def all(cls):
        return [
            cls.open_general_export_licence,
            cls.open_general_trade_control_licence,
            cls.open_general_transhipment_licence,
        ]

    @classmethod
    def as_options(cls):
        return [
            Option(key=ogl.id, value=f"{ogl.name} ({ogl.acronym})", description=ogl.description) for ogl in cls.all()
        ]

    @classmethod
    def get_by_id(cls, id):
        return next(ogl for ogl in cls.all() if ogl.id == id)
