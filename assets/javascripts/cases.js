function generateFlags(flags) {
	if (flags && flags.length) {
		var container = `<ol class="app-flags app-flags--list">`
		$.each(flags, function(i, item) {
			container = container + `
				<li class="app-flag app-flag--${item.colour} ${(i >= 3 ? "app-hidden--force" : "")}" ${(item.label ? `data-tooltip="${item.label}"` : ``)}>${item.name}</li>
			`
		})
		if (flags.length > 3) {
			return `${container}</ol><button onclick="expandFlags(this)" class="app-flags__expander"><span class="govuk-visually-hidden">Show more</span>${chevron} 3 of ${flags.length}</button></div>`
		} else {
			return `${container}</ol>`
		}
	} else {
		return `<p class="app-information-bar">No flags set</p>`
	}
}

function expandFlags(element) {
	$(element).prev().find(".app-hidden--force").slice(0, 5).removeClass("app-hidden--force").addClass("app-flag--animate");
	$(element).html(`<span class="govuk-visually-hidden">Show more</span>${chevron} ${$(element).prev().find(".app-flag").length - $(element).prev().find(".app-hidden--force").length} of ${$(element).prev().find(".app-flag").length}`)

	if (!$(element).prev().find(".app-hidden--force").length) {
		$(element).hide();
	}
}

function shortenName(first_name, last_name) {
	if (!first_name || !last_name ) {
		return "";
	}

	return first_name[0] + last_name[0];
}

function generateAssignments(assignments) {
	if (assignments.length) {
		var container = `<div class="app-assignments__container"><ul class="app-assignments__list">`;
		$.each(assignments.slice(0, 3), function(i, item) {
			container = container + `
				<li class="app-assignments__item" data-tooltip="${(item.user.first_name ? item.user.first_name + " " + item.user.last_name : item.user.email)}">
					<a class="app-assignments__item-link" href="/users/${item.user.id}/">${shortenName(item.user.first_name, item.user.last_name)}</a>
				</li>
			`;
		});
		if (assignments.length > 3) {
			container = container + `
				</ul><p class="app-assignments__link">${assignments.length - 3} more</p>
			`
		} else {
			container = container + `</ul>`;
		}
		return container + `</div>`;
	} else {
		return `<p class="app-information-bar">{% lcs 'cases.CasesListPage.NoContent.NO_GOODS_FLAGS' %}</p>`
	}
}

function generateSLA(percent) {
	var radius = 16;
	var circumference = 100.53096491487338;

	return `
		<div class="app-sla__container" data-tooltip="15 days have elapsed on this case">
			<svg class="app-sla" width="36" height="36">
				<circle class="app-sla__circle" stroke="black" stroke-width="3" fill="transparent" r="16" cx="18" cy="18" stroke-dasharray="${circumference} ${circumference}" stroke-dashoffset="${circumference - percent / 100 * circumference}"/>
			</svg>
			<span class="app-sla__text">7</span>
		</div>
	`
}

function generatePage(page, selected) {
	return `
		<li id="page-${page}" class="lite-pagination__list-item ${(selected ? "lite-pagination__list-item--selected" : "")}">
			${(selected ? page : `<a href="${params}&page=${page}">${page}</a>`)}
		</li>
	`
}

function generatePagination(currentPage, pages) {
	var pagesList = ``;
	var maxRange = 5

	// We want there to be a max_range bubble around the current page
	// eg current page is 6 and max range is 4, therefore we'll see 2 3 4 5 6 7 8 9 10
	var startRange = Math.max(1, currentPage - maxRange);
	var endRange = Math.min(pages, currentPage + maxRange);

	for (i = startRange; i <= endRange; i++) {
		pagesList = pagesList + generatePage(i, i == currentPage);
	}

	if (startRange >= 4) {
		pagesList = generatePage(1, false) + `<li class="lite-pagination__list-ellipsis">...</li>` + pagesList;
	} else if (startRange == 3) {
		pagesList = generatePage(1, false) + generatePage(2, false) + pagesList;
	} else if (startRange == 2) {
		pagesList = generatePage(1, false) + pagesList;
	}

	if (endRange == pages - 1) {
		pagesList = pagesList + generatePage(pages, false);
	} else if (endRange == pages - 2) {
		pagesList = pagesList + generatePage(pages - 1, false) + generatePage(pages, false);
	} else if (endRange <= pages - 3) {
		pagesList = pagesList + `<li class="lite-pagination__list-ellipsis">...</li>` + generatePage(pages, false);
	}

	var html = `
		<div class="lite-pagination__container">
			<${(currentPage != 1 ? "a": "p")} id="link-previous-page" href="${params}&page=${currentPage - 1}" id="link-previous-page" class="lite-pagination__navigation-link ${(currentPage != 1 ? "" : "lite-pagination__navigation-link--disabled")}">
				${previousSVG}
				<span>Previous page</span>
			</${(currentPage != 1 ? "a": "p")}>

			<ol class="lite-pagination__list">
				${pagesList}
			</ol>

			<${(currentPage != pages ? "a": "p")} id="link-next-page" href="${params}&page=${currentPage + 1}" id="link-next-page" class="lite-pagination__navigation-link ${(currentPage != pages ? "" : "lite-pagination__navigation-link--disabled")}">
				<span>Next page</span>
				${nextSVG}
			</${(currentPage != pages ? "a": "p")}>
		</div>
	`
	$("#main-content").append(html);
}
