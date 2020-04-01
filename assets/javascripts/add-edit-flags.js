tippy('.govuk-radios__input', {
    content(reference) {
        return reference.getAttribute('data-presentation-value');
    },
});
