from pytest_bdd import scenarios, given

scenarios("../features/view_mod_clearance.feature", strict_gherkin=False)


@given("a F680 Clearance is created")  # noqa
def an_f680_clearance_is_created(driver, apply_for_f680_clearance):
    pass
