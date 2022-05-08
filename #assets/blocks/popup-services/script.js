grummer.popupServices = {
	init() {
		this.initSlider(this.getSliderOptions());
	},
	open() {
		this.counter = 1;
		this.slidesOnPage = 6;
		this.mobilefilter = '';
		this.mobileList = $('.popup-services__mobile-list');

		this.setIsSelected();
		this.init();

		grummer.popup.open('_popup-services', true);
	},
	setIsSelected() {
		$('._popup-services__slide').removeClass('is-selected');

		grummer.currentServices.forEach(el => {
			$('._popup-services__slide').each(function () {
				if ($(this).data().id === el.id) {
					$(this).addClass('is-selected');
				}
			});
		});
	},
	initSlider(options = {}) {
		$('.popup-services__slider-services')
			.slick({
				...options,
				infinite: true,
				prevArrow: `<div class="prev-arrow slider-arrow">${arrow}</div>`, // from fragments
				nextArrow: `<div class="next-arrow slider-arrow">${arrow}</div>`,
			})
			.on('setPosition', () => {
				const options = this.getSliderOptions();
				$('.popup-services__slider-services').slick(
					'slickSetOption',
					options,
				);
			});
	},
	filter({category = ''}) {
		$('.popup-services__slider-services').slick('slickUnfilter');

		$('.popup-services__slider-services').slick(
			'slickFilter',
			(_, slide) => {
				if (category) {
					return $(slide).find(`._popup-services__slide.${category}`)
						.length;
				}

				return true;
			},
		);

		$('.popup-services__slider-services').slick('slickGoTo', 0);
	},
	filterServicesByCategory(category) {
		console.log('category', category)
		this.category = category;

		this.filter({
			category: this.category,
		});
	},
	getSliderOptions() {
		const viewport_width = window.innerWidth;

		if (viewport_width > 768) {
			return {
				slidesToShow: 4,
				slidesToScroll: 4,
				arrows: true,
			};
		} else if (viewport_width > 480) {
			return {
				slidesToShow: 3,
				slidesToScroll: 3,
				arrows: false,
			};
		} else {
			return {
				slidesToShow: 2,
				slidesToScroll: 2,
				arrows: false,
			};
		}
	},
	addService(service = '') {
		grummer.currentServices = [...grummer.currentServices, service];
		grummer.popupMain.open();
		$('.popup-services__slider-services').slick('unslick');
	},
	goBack() {
		$('.popup-services__slider-services').slick('unslick');
		grummer.popup.back('_popup-services')
	},
	close(e) {
		if (e && $(e.target).closest('.popup__content')[0]) return;
		
		$('.popup-services__slider-services').slick('unslick');
		grummer.popup.close('_popup-services')
	}
};
