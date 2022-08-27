class Validator {
	constructor(form) {
		this.$form = form;
		this.initCallbacks();
	}

	validate() {
		this.errors = [];
		let $formFields = $(this.$form).find('._field');
		let hasErrors = false;
		$formFields.each((fieldIndex, field) => {
			const $field = $(field);
			$field.removeClass('error');
			let callbacks = $field.data('call');

			if (!callbacks) return true;

			callbacks = callbacks.replace(/ +/g, ' ').trim().split(' ');
			callbacks.forEach(callback => {
				if (!this.callbacks[callback].call(this, $field)) {
					hasErrors = true;
					$field.addClass('error');
				}
			});
		});

		return !hasErrors;
	}

	initCallbacks() {
		this.callbacks = {
			/**
			 * @return bool
			 */
			phone($field) {
				let $input = $field.find('input');
				const regex =
					/^((\+7|7|8)+\([0-9]{3}\)[0-9]{3}\-[0-9]{2}\-[0-9]{2})$/;
				if (regex.test($input.val())) {
					$field.find('._error-msg').slideUp();
					return true;
				}

				this.setMessage($field);
				return false;
			},

			empty($field) {
				let $input = $field.find('input');
				let $textarea = $field.find('textarea');
				if ($input.val() == '' || $textarea.val() == '') {
					this.setMessage($field);
					return false;
				}
				$field.find('._error-msg').slideUp();
				return true;
			},
			selected($field) {
				let $input = $field.find('input');
				if ($input.val() == '') {
					this.setMessage($field);
					return false;
				}
				$field.find('._error-msg').slideUp();
				return true;
			},
			checked($field) {
				let $input = $field.find('input');
				let checker = false;
				$input.each(function () {
					if ($(this).prop('checked')) checker = true;
				});

				if (checker) {
					$field.find('._error-msg').slideUp();
					return true;
				}

				this.setMessage($field);
				return false;
			},
		};
	}

	setMessage($field) {
		const $errorMsg = $field.find('._error-msg');
		$errorMsg.html($field.data('msg'));
		$errorMsg.slideDown();
	}
}
