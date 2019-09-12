from pytest_bdd import then, scenarios
from pages.application_page import ApplicationPage


class ViewCaseDetails():
    scenarios('../features/case_view_details.feature', strict_gherkin=False)

    import logging
    log = logging.getLogger()
    console = logging.StreamHandler()
    log.addHandler(console)

    @then('I see an ultimate end user')
    def i_see_ultimate_end_user_on_page(driver, context):
        destinations_table = ApplicationPage(driver).get_text_of_ueu_table()
        destinations_table_lower = destinations_table.lower()
        assert "name" in destinations_table_lower
        assert "type" in destinations_table_lower
        assert "website" in destinations_table_lower
        assert "address" in destinations_table_lower
        assert context.ueu_type in destinations_table
        assert context.ueu_name in destinations_table
        assert context.ueu_website in destinations_table
        assert context.ueu_address in destinations_table
        assert context.ueu_country[0] in destinations_table

    @then('I see a consignee')
    def i_see_consignee_on_page(driver, context):
        destinations_table = ApplicationPage(driver).get_text_of_consignee_table()
        destinations_table_lower = destinations_table.lower()
        assert "name" in destinations_table_lower
        assert "type" in destinations_table_lower
        assert "website" in destinations_table_lower
        assert "address" in destinations_table_lower
        assert context.consignee['sub_type'] in destinations_table
        assert context.consignee['name'] in destinations_table
        assert context.consignee['website'] in destinations_table
        assert context.consignee['address'] in destinations_table
        assert context.consignee['country'][0] in destinations_table

    @then('I see a third party')
    def i_see_third_party_on_page(driver, context):
        destinations_table = ApplicationPage(driver).get_text_of_third_parties_table()
        destinations_table_lower = destinations_table.lower()
        assert "name" in destinations_table_lower
        assert "type" in destinations_table_lower
        assert "website" in destinations_table_lower
        assert "address" in destinations_table_lower
        assert context.third_party['sub_type'] in destinations_table
        assert context.third_party['name'] in destinations_table
        assert context.third_party['website'] in destinations_table
        assert context.third_party['address'] in destinations_table
        assert context.third_party['country'][0] in destinations_table
