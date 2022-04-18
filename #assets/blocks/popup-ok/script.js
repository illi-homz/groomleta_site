grummer.popupOk = {
	init() {
		this.$img = $('#popup-ok__img-img')
		this.$title = $('#popup-ok__img-title')
		this.$text = $('#popup-ok__img-text')
		this.staticURL = this.$img.attr('src-data')
	},
	gotoMain() {
		grummer.popup.close('_popup-ok');

		grummer.goToBlock('#header');
	},
	setPopupOkData({img, title = '', text = ''}) {
		this.$img.attr('src', this.staticURL + img)
		this.$title.text(title)
		this.$text.text(text)
	},
	open() {
		grummer.popup.open('_popup-ok');
		this.setTimeInterval()
	},
	setTimeInterval() {
		let time = 3
		const timeStr = num => `${num} сек`

		$('._popup-ok__timer-time').text(timeStr(time))


		let interval = setInterval(() => {
			$('._popup-ok__timer-time').text(`${--time} сек`)

			if (!time) {
				grummer.popup.close('_popup-ok')
				return clearInterval(interval)
			}
		}, 1000)
	}
};
