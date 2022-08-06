grummer.services = {
	category: '',
	animal: '',
	breed: '',
	breedNodes: null,

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
	filter({animal = '', category = '', breed = ''}) {
		$('._services__slider').slick('slickUnfilter');

		if (!animal && !category && !breed) {
			return;
		}

		$('._services__slider').slick('slickFilter', (_, slide) => {
			if (animal && category) {
				return $(slide).find(
					`._services__slide.category-${category}.${animal},._services__slide.any`,
				).length;
			}

			if (animal && breed) {
				const slideBreed = $(slide).find('._services__slide').attr('breed')?.toLowerCase();
				const isBreed = breed.toLowerCase().includes(slideBreed?.trim());
				const isAnimal = $(slide).find(
					`._services__slide.${animal},._services__slide.any`,
				).length;

				return isBreed && isAnimal
			}

			if (animal) {
				return $(slide).find(
					`._services__slide.${animal},._services__slide.any`,
				).length;
			}

			if (category) {
				return $(slide).find(`._services__slide.category-${category}`)
					.length;
			}

			if (breed) {
				const slideBreed = $(slide).find('._services__slide').attr('breed')?.toLowerCase();
				return breed.toLowerCase().includes(slideBreed?.trim());
			}

			return true;
		});

		$('._services__slider').slick('slickGoTo', 0);
	},
	filterServicesByAnimal(el, animal = null) {
		const $el = $(el);
		if ($el.hasClass('active')) return;
		$el.parent().children('div').removeClass('active');
		$el.addClass('active');

		this.animal = animal;

		this.filter({
			animal: this.animal,
			breed: this.breed,
			category: this.category,
		});
	},
	clearBreedFilter(el, e) {
		e.stopPropagation();
		$(el).parent().removeClass('active');
		this.animal = '';

		this.filter({
			animal: this.animal,
			breed: this.breed,
			category: this.category,
		});
	},
	filterServicesByCategory(category) {
		this.category = category;

		this.filter({
			animal: this.animal,
			breed: this.breed,
			category,
		});
	},
	filterServicesByBreed(breed) {
		// console.log('breed', breed)
		if (!breed) {
			$('._selected-text').text('Выберите породу')
		}
		
		this.breed = breed;

		this.filter({
			animal: this.animal,
			category: this.category,
			breed,
		});
	},
	filterOptionsByBreed(breed) {
		$('._g-select__find').val(breed)

		if (breed) {
			$('.g-select__find-close-btn').removeClass('hide')
		} else {
			$('.g-select__find-close-btn').addClass('hide')
		}
		
		if (!this.breedNodes) {
			this.breedNodes = $(
				'.services__categories ul.g-select__items .g-select__item._option',
			).clone();
		}

		$('.services__breeds ul.g-select__items').html('');

		this.breedNodes
			.filter((idx, el) => {
				return $(el)
					.data()
					.value.toLowerCase()
					.includes(breed.trim().toLowerCase());
			})
			.appendTo($('._services__breeds-items'));
	},

	openPopup(data) {
		grummer.currentServices = [data];
		grummer.popupMain.open();
	},
};
