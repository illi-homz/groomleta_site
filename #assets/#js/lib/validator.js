class Validator {
	constructor(form) {
		this.$form = form;
		this.initCallbacks();
	}

	validate() {
		this.errors = [];
		var $formFields = $(this.$form).find('._field');
		var hasErrors = false;
		$formFields.each((fieldIndex, field) => {
			var $field = $(field);
			$field.removeClass('error');
			var callbacks = $field.data('call');
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
				var $input = $field.find('input');
				var regex =
					/^((\+7|7|8)+\([0-9]{3}\)[0-9]{3}\-[0-9]{2}\-[0-9]{2})$/;

				if (regex.test($input.val())) {
					$field.find('._error-msg').slideUp();
					return true;
				}

				this.setMessage($field);
				return false;
			},

			empty($field) {
				var $input = $field.find('input');
				var $textarea = $field.find('textarea');

				if ($input.val() == '' || $textarea.val() == '') {
					this.setMessage($field);
					return false;
				}

				$field.find('._error-msg').slideUp();
				return true;
			},

			selected($field) {
				var $input = $field.find('input');

				if ($input.val() == '') {
					this.setMessage($field);
					return false;
				}

				$field.find('._error-msg').slideUp();
				return true;
			},

			checked($field) {
				var $input = $field.find('input');
				var checker = false;
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
		var $errorMsg = $field.find('._error-msg');
		$errorMsg.html($field.data('msg'));
		$errorMsg.slideDown();
	}
}
