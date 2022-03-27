grummer.promo = {
  init() {
	this.slider = $("._promo__slider");
    this.initSlider();
  },
  initSlider() {
    const slickParams = {
      mobileFirst: true,
      infinite: true,
      slidesToShow: 1,
      slidesToScroll: 1,
      autoplay: true,
      autoplaySpeed: 4000,
      focusOnSelect: true,
      fade: true
    };

    this.slider.slick(slickParams);
  },
};
