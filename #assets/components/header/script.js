"use strict";

grummer.header = {
	init() {
		this.changeBg();
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
};
