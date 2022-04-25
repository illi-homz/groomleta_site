grummer.navbar = {
	init() {
		this.dataInit();
	},
	dataInit() {
		this.menu = $('.navbar__mobile-menu');
		this.burger = $('.navbar__burger');
	},
	toggleMenu() {
		this.menu.slideToggle(300);
		this.burger.toggleClass('active');

		$('body').hasClass('lock')
			? $('body').removeClass('lock')
			: $('body').addClass('lock');
	},
	goToBlock(...args) {
		this.toggleMenu();
		const href = $(args[0]).attr('href')

		if (!href.startsWith('/')) {
			grummer.goToBlock(...args);
		}
	},
};
