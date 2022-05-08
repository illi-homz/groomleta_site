grummer.services = {
	category: '',
	animal: '',

	init() {
		this.initSlider(this.getSliderOptions());
	},
	initSlider(options = {}) {
		$('._services__slider')
			.slick({
				...options,
				infinite: true,
				prevArrow: `<div class="prev-arrow slider-arrow">${arrow}</div>`,
				nextArrow: `<div class="next-arrow slider-arrow">${arrow}</div>`,
			})
			.on('setPosition', () => {
				const options = this.getSliderOptions();
				$('._services__slider').slick('slickSetOption', options);
			});
	},
	getSliderOptions() {
		const viewport_width = window.innerWidth;

		if (viewport_width > 993) {
			return {
				slidesToShow: 6,
				slidesToScroll: 6,
				arrows: true,
			};
		} else if (viewport_width > 768) {
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
	filter({animal = '', category = ''}) {
		$('._services__slider').slick('slickUnfilter');

		if (!animal && !category) {
			return
		};

		$('._services__slider').slick('slickFilter', (_, slide) => {
			if (animal && category) {
				return $(slide).find(
					`._services__slide.category-${category}.${animal},._services__slide.all`,
				).length;
			}

			if (animal) {
				return $(slide).find(
					`._services__slide.${animal},._services__slide.all`,
				).length;
			}

			if (category) {
				return $(slide).find(`._services__slide.category-${category}`).length;
			}

			return true;
		});

		$('._services__slider').slick('slickGoTo', 0);
	},
	filterServicesByBreed(el, animal = null) {
		const $el = $(el);
		if ($el.hasClass('active')) return;
		$el.parent().children('div').removeClass('active');
		$el.addClass('active');

		this.animal = animal;

		this.filter({
			animal: this.animal,
			category: this.category,
		});
	},
	clearBreedFilter(el, e) {
		e.stopPropagation();
		$(el).parent().removeClass('active');
		this.animal = '';

		this.filter({
			animal: this.animal,
			category: this.category,
		});
	},
	filterServicesByCategory(category) {
		this.category = category;

		this.filter({
			animal: this.animal,
			category,
		});
	},

	openPopup(data) {
		grummer.currentServices = [data];
		grummer.popupMain.open();
	},
};
