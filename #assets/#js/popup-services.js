grummer.popupServices = {
  init() {
    this.servicesList = grummer.animal
      ? [
        ...grummer.servicesList[grummer.animal],
        ...grummer.servicesList.additional,
      ]
      : Object.keys(grummer.servicesList).reduce((acc, key) => {
          return [...acc, ...grummer.servicesList[key]];
        }, []);

    this.setCategories(grummer.categories);

    this.sliderList = $(".popup-services__slider-services")
      .removeClass("slick-initialized slick-slider")
      .html("");

    this.sliderTemplate = $.trim($("#popup-services__slider-temp").html());

    this.setSlides(
      this.servicesList.filter((el) => el.category !== "add-services"),
      this.sliderList,
      this.sliderTemplate
    );

    this.initSlider(this.sliderList);
    // this.initSlider(this.sliderListAdd);
  },
  open() {
    this.counter = 1;
    this.slidesOnPage = 6;
    this.mobilefilter = "";
    this.mobileList = $(".popup-services__mobile-list");

    this.init();

    grummer.popup.open("_popup-services");
  },
  setCategories(arr) {
    const list = $(".popup-services .g-select__items");
    const template = $.trim(
      $(".popup-services .popup-services__filter-temp").html()
    );

    list.html(
      arr.reduce((acc, item) => {
        return (acc += template
          .replace(/{{title}}/gi, item.title)
          .replace(/{{value}}/gi, item.value)
          // .replace(/{{icon}}/gi, item.icon)
          );
      }, "")
    );
  },
  filter(arr) {
    this.setSlides(arr, this.sliderList, this.sliderTemplate);
    this.sliderList.removeClass("slick-initialized slick-slider");
    this.initSlider(this.sliderList);
  },
  filterServices(val, type) {
    return this.servicesList.filter((service) => {
      return service[type] === val;
    });
  },
  filterServicesByCategory(val) {
    this.mobilefilter = val;
    this.counter = 1;

    !val
      ? this.filter(
          this.servicesList.filter((el) => el.category !== "add-services")
        )
      : this.filter(this.filterServices(val, "category"));
  },
  createHtmlList(arr, template) {
    return arr.reduce((acc, slide) => {
      const isSelected = !!grummer.currentServices.find(el => el.id === slide.id)

      return (acc += template
        .replace(/{{is-selected}}/gi, isSelected ? 'is-selected' : '')
        .replace(/{{title}}/gi, slide.title)
        .replace(/{{text}}/gi, slide.text)
        .replace(/{{price}}/gi, slide.price)
        .replace(/{{time}}/gi, slide.time)
        .replace(/{{img}}/gi, slide.img));
    }, "");
  },
  setSlides(slides, list, template) {
    list.html("");
    list.append(this.createHtmlList(slides, template));
  },
  initSlider($el) {
    $el.slick({
      infinite: true,
      mobileFirst: true,
      slidesToShow: 2,
      slidesToScroll: 2,
      prevArrow: `<div class="prev-arrow slider-arrow">${arrow}</div>`, // from fragments
      nextArrow: `<div class="next-arrow slider-arrow">${arrow}</div>`,
      responsive: [
        {
          breakpoint: 480,
          settings: {
            slidesToShow: 3,
            slidesToScroll: 3,
            // infinite: true
          }
        },
        {
          breakpoint: 900,
          settings: {
            slidesToShow: 4,
            slidesToScroll: 4,
            // infinite: true
          }
        }
      ]
    });
  },
  addService(title, text) {
    const service = this.servicesList.find((obj) => {
      return obj.title === title && obj.text === text;
    });

    if (!grummer.currentServices.includes(service)) {
      grummer.currentServices.push(service);
    }

    grummer.popupMain.open();
  },
};
