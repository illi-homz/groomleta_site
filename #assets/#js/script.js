"use strict";



const grummer = {
	animal: null,
	currentServices: [],
	currentBreed: undefined,
	breesTemplate: null,
	
	goToBlock(target, event) {
		if (event) event.preventDefault();
		
		$("html,body").animate({
			scrollTop:
			typeof target === "string"
				? target
				: $(target.hash).offset().top,
		});
	},
};

@@include('@@webRoot/#assets/#js/lib/jquery.min.js');
@@include('@@webRoot/#assets/#js/lib/slick.min.js');
@@include('@@webRoot/#assets/#js/lib/webp.js');
@@include('@@webRoot/#assets/#js/lib/validator.js');
@@include('@@webRoot/#assets/#js/lib/maskedinput.min.js');
@@include('@@webRoot/#assets/#js/lib/air-datepicker.js');
@@include('@@webRoot/#assets/#js/lib/tlg.js');

@@include('@@webRoot/#assets/#js/fragments.js');
@@include('@@webRoot/#assets/#js/popup.js');
@@include('@@webRoot/#assets/#js/g-select.js');

@@include('@@webRoot/#assets/components/header/script.js');
@@include('@@webRoot/#assets/components/navbar/script.js');

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
	$("._input-phone").mask("+7(999)999-99-99");
	this.popup.init();
	this.header.init();
	this.services.init();
	this.ourworks.init();
	this.questions.init();
	this.promo.init();
	this.feedbacks.init();
	this.popupOk.init();
	this.navbar.init();
};

$(document).ready(() => {
	grummer.init();
});
