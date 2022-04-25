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
	goToBlock(target, event, isMobile) {
		const href = $(target).attr('href')

		isMobile && this.toggleMenu();
		!href.startsWith('/') && grummer.goToBlock(target, event);
	},
};
