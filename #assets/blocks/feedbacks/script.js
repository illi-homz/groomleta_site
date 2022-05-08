grummer.feedbacks = {
	init() {
		this.initSlider();
	},
	initSlider() {
		$('.feedbacks__slider').slick({
			mobileFirst: true,
			infinite: false,
			dots: true,
			arrows: false,
			slidesToShow: 1,
			slidesToScroll: 1,
			responsive: [
				{
					breakpoint: 768,
					settings: {
						infinite: true,
						arrows: true,
						prevArrow: `<div class="prev-arrow slider-arrow">${arrow}</div>`,
						nextArrow: `<div class="next-arrow slider-arrow">${arrow}</div>`,
					},
				},
			],
		});
	},
};
