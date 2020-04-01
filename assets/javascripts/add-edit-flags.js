tippy('.govuk-radios__input', {
    content(reference) {
        return reference.getAttribute('data-presentation-value');
    },
});

$("#pane_label").addClass("govuk-inset-text");