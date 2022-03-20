"use strict";

grummer.services = {
	sliderList: [],
	sliderTemplate: null,
	currentServicesList: [],
	currentCategory: null,

	async init() {
		await this.getServices()
		this.sliderList = $("._services__slider");
		this.sliderTemplate = $.trim($("#services__slider-temp").html());
		this.setSlides(null, this.sliderList, this.sliderTemplate);
		this.initSlider();
	},
	async getServices() {
		const services = await fetch("/api/services-list", {
			method: "GET",
		})
			.then(response => response.json())
			.catch(e => console.log('getCategories exeption:', e))

		grummer.servicesList = services
	},
	initSlider() {
		$(".services__slider").slick({
			infinite: true,
			slidesToShow: 6,
			slidesToScroll: 6,
			// prevArrow: '<div class="prev-arrow slider-arrow"><img src="img/arrow.svg"/></div>',
			// nextArrow: '<div class="next-arrow slider-arrow"><img src="img/arrow.svg"/></div>',
			prevArrow: `<div class="prev-arrow slider-arrow">${arrow}</div>`,
			nextArrow: `<div class="next-arrow slider-arrow">${arrow}</div>`,
			responsive: [
				{
					breakpoint: 993,
					settings: {
						slidesToShow: 4,
						slidesToScroll: 4,
					},
				},
				{
					breakpoint: 768,
					settings: {
						slidesToShow: 3,
						slidesToScroll: 3,
						arrows: false,
					},
				},
				{
					breakpoint: 480,
					settings: {
						slidesToShow: 2,
						slidesToScroll: 2,
						arrows: false,
					},
				},
			],
		});
	},
	setSlides(arr, list, template) {
		list.html("");
		let frag = "";

		let slides = arr ? arr : null;

		// if (!slides) {
		// 	if (grummer.animal) {
		// 		this.currentServicesList = [
		// 			...grummer.servicesList[grummer.animal],
		// 			...grummer.servicesList.additional,
		// 		];
		// 	} else {
		// 		this.currentServicesList = Object.keys(
		// 			grummer.servicesList
		// 		).reduce((acc, key) => {
		// 			return [...acc, ...grummer.servicesList[key]];
		// 		}, []);
		// 	}

		// 	slides = this.currentServicesList;
		// }

		slides = grummer.servicesList;

		// if (this.currentCategory) {
		// 	slides = slides.filter((service) => {
		// 		return service.category === this.currentCategory;
		// 	});
		// }

		const templatedSlides = slides.map((slide, i) => {
			return template
				.replace(/{title}/gi, slide.title)
				.replace(/{text}/gi, slide.text)
				.replace(/{price}/gi, slide.price)
				.replace(/{time}/gi, slide.time)
				.replace(/{img}/gi, slide.img)
		})

		list.append(templatedSlides.join());
		// list.append(frag);
	},

	setBreed(val) {
		this.breed = val;
	},

	filter(arr) {
		this.setSlides(arr, this.sliderList, this.sliderTemplate);
		this.sliderList.removeClass("slick-initialized slick-slider");
		this.initSlider();
	},

	filterServices(val, type = "category") {
		if (!val) {
			return this.currentServicesList;
		}

		return this.currentServicesList.filter(
			(service) => service[type] === val
		);
	},
	filterServicesByBreed(el, animal = null) {
		const $el = $(el);
		if ($el.hasClass("active")) return;

		$el.parent().children("div").removeClass("active");

		$el.addClass("active");

		grummer.animal = animal;

		this.filter();
	},
	clearBreedFilter(el, e) {
		e.stopPropagation();
		$(el).parent().removeClass("active");
		grummer.animal = null;
		this.filter();
	},

	filterServicesByCategory(category) {
		this.currentCategory = category;
		const filteredServicesByCategory = this.filterServices(category);

		if (
			filteredServicesByCategory.length ===
			this.currentServicesList.length
		) {
			this.cleanFilter();
		} else {
			// this.showCleaner();
			$(".services__categories._select").addClass("active");
		}

		this.filter([
			...filteredServicesByCategory,
			...grummer.servicesList.additional,
		]);
	},

	cleanFilter() {
		this.currentCategory = null;
		this.filter();
		// this.hideCleaner();

		const $categories = $(".services__categories");
		$categories.find("._selected-text").html("Выберите категорию");

		$categories.find("._option").removeClass("active");
		$(".services__categories._select").removeClass("active");
	},

	// showCleaner() {
	//   $(".services__filters-cleaner").addClass("active");
	// },
	// hideCleaner() {
	//   $(".services__filters-cleaner").removeClass("active");
	// },

	openPopup(title) {
		const service = this.currentServicesList.find((obj) => {
			return obj.title === title;
		});
		const breed = grummer.breeds.find((obj) => {
			return obj.value === this.breed;
		});

		grummer.currentServices = [service];
		if (breed) grummer.currentBreed = breed.title;

		grummer.popupMain.open();
	},
};
