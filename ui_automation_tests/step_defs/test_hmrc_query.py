from pytest_bdd import given, scenarios

scenarios("../features/hmrc_query.feature", strict_gherkin=False)


@given("I create a hmrc query")  # noqa
def create_hmrc_query(driver, apply_for_hmrc_query, context):
    pass
