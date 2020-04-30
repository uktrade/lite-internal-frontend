let team = $("#team");

function filterSelectOptions(team_value, default_to_select) {
    // if team changes, set default_queue to 'select' and filter out other team queues
    let default_queue = $("#default_queue");
    default_queue.children("option[data-attribute!='None']").hide();
    default_queue.children("option[data-attribute='" + team_value + "'], option[value='']").show();

    if (default_to_select === true) {
        default_queue.val("");
    }
}

team.change(function () {
    filterSelectOptions(team.val(), true)
});

team.ready(function () {
    filterSelectOptions(team.val(), false)
});
