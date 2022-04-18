grummer.popupFeedback = {
	open() {
		this.$popupMain = $('._popup-feedback');
		grummer.popup.open(this.$popupMain);
	},
	async submit(form, event) {
		event.preventDefault();

		const validator = new Validator(form);
		const v = validator.validate();
		if (!v) return;

		const csrf = form.csrfmiddlewaretoken.value;
		const msg = {
			name: form.name.value,
			lastname: form.lastname.value,
			comment: form.comment.value,
		};
		const res = await grummer.tlg.sendFeedback(msg, csrf);

		if (res.status === 'success') {
			setTimeout(() => {
				grummer.popupOk.setPopupOkData({
					img: 'img/feedback.svg',
					title: 'Спасибо за отзыв!',
				});
				grummer.popupOk.open();
			}, 300);
		}

		form.reset();
	},

	changeCounter(fieldInput) {
		const textLength = fieldInput.value.length;
		$(fieldInput)
			.parent('._field')
			.siblings('._popup-main__form-field-counter')
			.find('span')
			.html(textLength);
	},
};
