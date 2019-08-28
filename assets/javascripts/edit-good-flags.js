var buttonGiveAdvice = $("#button-edit-goods-flags")

function setEditGoodsFlagsAbility() {
	// Disable the give advice button unless a checkbox is selected
	if ($("input[name='goods']:checked").length == 0) {
		disableButton(buttonGiveAdvice)
	} else {
		enableButton(buttonGiveAdvice)
	}
}

setEditGoodsFlagsAbility();

$("input[type='checkbox']").change(function() {
	setEditGoodsFlagsAbility();
});
