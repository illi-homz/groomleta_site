grummer.popupServices = {
	breed: '',
	breedNodes: null,

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
				if (+$(this).data().id === +el.id) {
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
	filter({animal = '', category = '', breed = ''}) {
		$('.popup-services__slider-services').slick('slickUnfilter');

		if (!animal && !category && !breed) {
			return
		};

		$('.popup-services__slider-services').slick(
			'slickFilter',
			(_, slide) => {
				if (animal && category) {
					return $(slide).find(
						`._popup-services__slide.category-${category}.${animal},._popup-services__slide.any`,
					).length;
				}

				if (animal && breed) {
					const slideBreed = $(slide).find('._popup-services__slide').attr('breed')?.toLowerCase();
					const isBreed = breed.toLowerCase().includes(slideBreed?.trim());

					const isAnimal = $(slide).find(
						`._popup-services__slide.${animal},._popup-services__slide.any`,
					).length;
	
					return isBreed && isAnimal
				}
			
				if (animal) {
					return $(slide).find(
						`._popup-services__slide.${animal},._popup-services__slide.any`,
					).length;
				}
				
				if (category) {
					return $(slide).find(`._popup-services__slide.${category}`)
						.length;
				}

				if (breed) {
					const slideBreed = $(slide).find('._popup-services__slide').attr('breed')?.toLowerCase();
					return breed.toLowerCase().includes(slideBreed?.trim());
				}

				return true;
			},
		);

		$('.popup-services__slider-services').slick('slickGoTo', 0);
	},
	filterServicesByCategory(category) {
		this.category = category;

		this.filter({
			animal: this.animal,
			breed: this.breed,
			category,
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
		this.filterServicesByBreed('')
		this.filterOptionsByBreed('')
		$('.popup-services__slider-services').slick('unslick');
		grummer.popup.back('_popup-services')
	},
	close(e) {
		if (e && $(e.target).closest('.popup__content')[0]) return;

		this.filterServicesByBreed('')
		this.filterOptionsByBreed('')
		$('.popup-services__slider-services').slick('unslick');
		grummer.popup.close('_popup-services')
	},

	filterServicesByAnimal(el, animal = null) {
		const $el = $(el);
		if ($el.hasClass('active')) return;
		$el.parent().children('div').removeClass('active');
		$el.addClass('active');

		this.animal = animal;

		this.filter({
			animal: this.animal,
			category: this.category,
			breed: this.breed,
		});
	},
	clearBreedFilter(el, e) {
		e.stopPropagation();
		$(el).parent().removeClass('active');
		this.animal = '';

		this.filter({
			animal: this.animal,
			category: this.category,
			breed: this.breed,
		});
	},

	filterServicesByBreed(breed) {
		if (!breed) {
			$('.popup-services__breeds ._selected-text').text('Выберите породу')
		}
		
		this.breed = breed;

		this.filter({
			animal: this.animal,
			category: this.category,
			breed,
		});
	},
	filterOptionsByBreed(breed) {
		$('.popup-services__breeds ._g-select__find').val(breed)

		if (breed) {
			$('.popup-services__breeds .g-select__find-close-btn').removeClass('hide')
		} else {
			$('.popup-services__breeds .g-select__find-close-btn').addClass('hide')
		}
		
		if (!this.breedNodes) {
			this.breedNodes = $(
				'.popup-services__breeds ul.g-select__items .g-select__item._option',
			).clone();
		}

		$('.popup-services__breeds ul.g-select__items').html('');

		this.breedNodes
			.filter((idx, el) => {
				return $(el)
					.data()
					.value.toLowerCase()
					.includes(breed.trim().toLowerCase());
			})
			.appendTo($('._popup-services__breeds-items'));
	},

};
