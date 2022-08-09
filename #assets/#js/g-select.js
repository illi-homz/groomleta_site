'use strict';

grummer.gSelect = {
	open($select) {
		$select.children('._options').first().slideDown(300);
		$select.toggleClass('opened');

		$(window).on('click', () => {
			this.close($select);
		});
		$select.on('click', e => {
			e.stopPropagation();
		});
	},
	close($select) {
		$select.children('._options').first().slideUp(300);
		$select.toggleClass('opened');

		$(window).off('click');
		$select.off('click');

		$select.find('._dog-select').addClass('hide');
		$select.find('span._selected-text').removeClass('hide');
	},
	toggle(instance) {
		let $select = $(instance).parents('._select');

		if (!$select.hasClass('opened')) {
			this.open($select);
		} else {
			this.close($select);
		}
	},
	setName($select, name) {
		$select.find('._selected-text').html(name);
	},
	setInputValue($select, value) {
		$select.find('._select-input').val(value).trigger('change');
	},
	selectItem(instance) {
		const $inst = $(instance);
		const $select = $inst.parents('._select');
		$select.removeClass('error');
		$select.find('._option').removeClass('active');

		$inst.addClass('active');
		const name = $inst.text();
		const selectedValue = $inst.data('value');

		this.setName($select, name);
		this.setInputValue($select, selectedValue);
		this.close($select);
	},
	stopPropagation(event) {
		event.stopPropagation();
	}
};
