"use strict";

grummer.header = {
	init() {
		this.dataInit();
		this.changeBg();
	},
	dataInit() {
		this.menu = $(".header__mobile-menu");
		this.burger = $(".header__burger");
	},
	changeBg() {
		let count = 1;
		const timeChange = 9000;
		const $bgs = $("._header__bg");
		const arrLen = $bgs.length;

		return setInterval(() => {
			if (count > arrLen - 1) count = 0;
			$bgs.removeClass("active");
			$bgs[count].classList.add("active");
			count++;
		}, timeChange);
	},
	toggleMenu() {
		this.menu.slideToggle(300);
		this.burger.toggleClass("active");

		$("body").css("overflow") === "visible"
			? $("body").css({ overflow: "hidden" })
			: $("body").css({ overflow: "auto" });
	},
};
