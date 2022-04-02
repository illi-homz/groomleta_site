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
};
