grummer.callback = {
	init() {
		$('._input-phone').mask('+7(999)999-99-99');
	},
	async submit(form, event) {
		event.preventDefault();

		const validator = new Validator(form);

		const v = validator.validate();

		if (!v) return;

		const csrf = form.csrfmiddlewaretoken.value

		let msg = "*Заказ звонка*\n\n";
		msg += grummer.tlg.createMsg(form).replace("name", "Клиент").replace("tel", "Тел");
	
		const res = await grummer.tlg.sendMessage(msg, csrf);

		if (res.status === 'success') {
			setTimeout(() => {
				grummer.popup.open('_popup-ok');
			}, 100);
		}

		form.reset();
	},
};
