grummer.popup = {
	init() {
		this.body = $('body');
		this.lockPadding = $('.lock-padding'); // for fixed elements

		this.unlock = true;
		this.timeOut = 300;

		this.closeOnEsc();
	},
	open(popup, noClickEvent) {
		if (!(popup && this.unlock)) return;

		this.$popupActive = $('.popup.open');

		// Close old popup
		!!this.$popupActive[0]
			? this.close(this.$popupActive, false)
			: this.bodyLock();

		let $popup;

		// Open
		typeof popup === 'string'
			? ($popup = $(`.${popup}`).addClass('open'))
			: ($popup = popup.addClass('open'));

		if (!noClickEvent) {
			// Close on click outside
			$popup.on('click', e => {
				if (!$(e.target).closest('.popup__content')[0]) this.close($popup);
			});
		}
	},
	close(popup, doUnlock = true) {
		if (this.unlock) {
			typeof popup === 'string'
				? $(`.${popup}`).removeClass('open')
				: popup.removeClass('open');

			if (doUnlock) this.bodyUnlock();
		}

		this.body.css({overflow: 'auto'});
	},
	back(popup, cb) {
		this.close(popup, false);
		if (this.$popupActive) this.$popupActive.addClass('open');
		typeof cb === 'function' && cb()
	},
	bodyLock() {
		const lockPaddingValue =
			window.innerWidth - this.body.innerWidth() + 'px';

		this.body.css({paddingRight: lockPaddingValue});
		this.body.addClass('lock');

		if (this.lockPadding.length) {
			this.lockPadding.each((i, el) => {
				$(el).css({paddingRight: lockPaddingValue});
			});
		}

		this.unlock = false;
		setTimeout(() => {
			this.unlock = true;
		}, this.timeOut);
	},
	bodyUnlock() {
		setTimeout(() => {
			if (this.lockPadding.length) {
				this.lockPadding.each((i, el) => {
					$(el).css({paddingRight: '0px'});
				});
			}
			this.body.css({paddingRight: '0px'});
			this.body.removeClass('lock');
		}, this.timeOut);

		this.unlock = false;
		setTimeout(() => {
			this.unlock = true;
		}, this.timeOut);
	},
	closeOnEsc() {
		$(':root').on('keydown', e => {
			if (e.which === 27) this.close('popup.open');
		});
	},
};
