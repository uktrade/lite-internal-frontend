function showProvisoModal() {
	LITECommon.Modal.showModal('Pick from provisos', $( '#modal-proviso-picker' ).html(), false, true, {maxWidth: '500px'});
	return false;
};

function showPreviewModal(item) {
	var title = $(item).data( 'title' );
	var text = $('<div>').text($(item).data( 'text' )).html();
	var lastUpdated = $(item).data( "last-updated" );

	var previewHtml = '<div class="app-picklist-picker-preview">' +
						  '<div class="app-picklist-picker-preview__text">' +
							  '<p id="picker-preview-text" class="govuk-body-m">' + text + '</p>' +
						  '</div>' +
						  '<div class="app-picklist-picker-preview__controls">' +
							  '<button onclick="setProvisoText();" type="submit" class="govuk-button" data-module="govuk-button">' +
								  'Use template' +
							  '</button>' +
						   '</div>' +
					  '</div>'

	LITECommon.Modal.showModal(title, previewHtml, false, true);
	return false;
};

function addSlashes( str ) {
    return (str + '').replace(/[\\"']/g, '\\$&').replace(/\u0000/g, '\\0');
}

function setProvisoText() {
	$('#textarea-proviso').val($('#picker-preview-text').text()).keyup();
	LITECommon.Modal.closeAllModals();
}
