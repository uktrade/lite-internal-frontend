$(".lite-expandable-textarea-controls").addClass("lite-expandable-textarea-controls--hidden");
$(".case_note-warning").addClass("govuk-hint--hidden");

$("#case_note").on('input propertychange paste', function() {
	if ($(this).val() != '') {
		$(".lite-expandable-textarea-controls").removeClass("lite-expandable-textarea-controls--hidden");
	} else {
		$(".lite-expandable-textarea-controls").addClass("lite-expandable-textarea-controls--hidden");
	}

	if ($(this).val().length > 1200) {
		$("#case_note-warning").text("You have " + (2200 - $(this).val().length) + " character" + pluralize(2200 - $(this).val().length) + " remaining");
	} else {
		$("#case_note-warning").text("You can enter up to 2200 characters");
	}

	if ($(this).val().length <= 1) {
		$("#button-post-note").addClass("govuk-button--disabled");
		$("#button-post-note").attr("disabled", true);
	}

	if ($(this).val().length > 2200) {
		$("#case_note-warning").removeClass("govuk-hint");
		$("#case_note-warning").addClass("govuk-error-message");
		$("#case_note-warning").text("You have " + ($(this).val().length - 2200) + " character" + pluralize($(this).val().length - 2200) + " too many");
		$("#button-post-note").addClass("govuk-button--disabled");
		$("#button-post-note").attr("disabled", true);
		$(".lite-expandable-textarea").addClass("lite-expandable-textarea--warning");
	} else {
		$("#case_note-warning").removeClass("govuk-error-message");
		$("#case_note-warning").addClass("govuk-hint");
		$(".lite-expandable-textarea").removeClass("lite-expandable-textarea--warning");
		if ($(this).val().length > 1) {
			$("#button-post-note").removeClass("govuk-button--disabled");
			$("#button-post-note").attr("disabled", false);
		}
	}
});
