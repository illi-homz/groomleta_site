grummer.callback = {
	init() {},
	async submit(form, event) {
		event.preventDefault();

		const validator = new Validator(form);

		const v = validator.validate();

		if (!v) return;

		const csrf = form.csrfmiddlewaretoken.value
		const msg = {
			name: form.name.value,
			tel: form.tel.value
		}
		const res = await grummer.tlg.sendCallback(msg, csrf);

		if (res.status === 'success') {
			setTimeout(() => {
				grummer.popupOk.setPopupOkData({
					img: 'img/ok.svg',
					title: 'Заявка принята',
					text: 'Ожидайте звонка в течение минуты',
				});
				grummer.popupOk.open();
			}, 100);
		}

		form.reset();
	},
};
