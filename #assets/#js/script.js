"use strict";

@@include('@@webRoot/#assets/#js/lib/jquery.min.js');
@@include('@@webRoot/#assets/#js/lib/slick.min.js');
@@include('@@webRoot/#assets/#js/lib/webp.js');
@@include('@@webRoot/#assets/#js/lib/validator.js');
@@include('@@webRoot/#assets/#js/lib/maskedinput.min.js');
@@include('@@webRoot/#assets/#js/lib/air-datepicker.js');

const grummer = {
	animal: null,
	currentServices: [],
	currentBreed: undefined,
	breesTemplate: null,

	goToBlock(target, event, isMobile = false) {
		if (event) event.preventDefault();
		if (isMobile) this.header.toggleMenu();

		$("html,body").animate({
			scrollTop:
				typeof target === "string"
					? target
					: $(target.hash).offset().top,
		});
	},
};

@@include('@@webRoot/#assets/#js/fragments.js');
@@include('@@webRoot/#assets/#js/lib/tlg.js');
@@include('@@webRoot/#assets/#js/popup.js');
@@include('@@webRoot/#assets/#js/popup-services.js');

@@include('@@webRoot/#assets/#js/store.js');
@@include('@@webRoot/#assets/#js/g-select.js');
@@include('@@webRoot/#assets/components/header/script.js');

@@include('@@webRoot/#assets/blocks/services/script.js');
@@include('@@webRoot/#assets/blocks/ourworks/script.js');
@@include('@@webRoot/#assets/blocks/questions/script.js');
@@include('@@webRoot/#assets/blocks/promo/script.js');
@@include('@@webRoot/#assets/blocks/feedbacks/script.js');
@@include('@@webRoot/#assets/blocks/callback/script.js');
@@include('@@webRoot/#assets/blocks/popup_feedback/script.js');
@@include('@@webRoot/#assets/blocks/popup-ok/script.js');
@@include('@@webRoot/#assets/blocks/popup-main/script.js');
@@include('@@webRoot/#assets/blocks/popup-services/script.js');

grummer.init = function () {
	this.store.init();

	$("._input-phone").mask("+7(999)999-99-99");

	this.tlg.init();
	this.popup.init();
	// this.popupServices.init()
	
	this.header.init();
	this.services.init();
	this.ourworks.init();
	this.questions.init();
	this.promo.init();
	this.feedbacks.init();
	this.popupOk.init();
	// grummer.popupMain.init()
};

$(document).ready(() => {
	grummer.init();
});
