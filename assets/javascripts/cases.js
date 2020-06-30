function openTableFold(element) {
	$(element).parent().parent().find(".app-expanded-row__item, .app-expanded-row__item--invert").toggle();
	$(element).toggleClass("lite-expand__control--open");
	updateTableFoldControl();
	return false;
}

function updateTableFoldControl() {
	if ($(".lite-expand__control").length == $(".lite-expand__control--open").length) {
		$("#link-open-all-table-folds").addClass("lite-expand__base-control--open");
	} else {
		$("#link-open-all-table-folds").removeClass("lite-expand__base-control--open");
	}
}

function toggleTableFold() {
	if ($(".lite-expand__control").length == $(".lite-expand__control--open").length) {
		$(".app-expanded-row__item").hide();
		$(".app-expanded-row__item--invert").show();
		$(".lite-expand__control").removeClass("lite-expand__control--open");
	} else {
		$(".app-expanded-row__item").show();
		$(".app-expanded-row__item--invert").hide();
		$(".lite-expand__control").addClass("lite-expand__control--open");
	}

	updateTableFoldControl();
	return false;
}

function generatePagination(page, pages) {
	return `
		<div class="lite-pagination__container">
			<a id="link-previous-page" href="{{ previous_link_url }}" id="link-previous-page" class="lite-pagination__navigation-link">
				{% svg 'previous' %}
				<span>Previous page</span>
			</a>

			<ol class="lite-pagination__list">
				{% for item in pages %}
					{% if item.type == 'page_item' %}
						<li id="page-{{ item.number }}" class="lite-pagination__list-item {% if item.selected %}lite-pagination__list-item--selected{% endif %}">
							{% if item.selected %}
								{{ item.number }}
							{% else %}
								<a href="{{ item.url }}">
									{{ item.number }}
								</a>
							{% endif %}
						</li>
					{% elif item.type == 'page_ellipsis' %}
						<li class="lite-pagination__list-ellipsis">
							{{ item.text }}
						</li>
					{% endif %}
				{% endfor %}
			</ol>

			<a id="link-next-page" href="{{ next_link_url }}" id="link-next-page" class="lite-pagination__navigation-link">
				<span>Next page</span>
				{% svg 'next' %}
			</a>
		</div>
	{% endif %}
	`
}
