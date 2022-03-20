grummer.promo = {
  banners: [
    {
      img: "banner_1.png",
      title: "Пенсионерам ",
      text: "дополнительная скидка",
      class: "left",
      value: "5%",
    },
    {
      img: "banner_2.png",
      title: "Скидка для друга 10%",
      text: "а вам 10% на следующее посещение",
      class: "right",
      value: "",
    },
    {
      img: "banner_3.png",
      title: "Скидка 10%",
      text: "на пятое посещение",
      class: " costom",
      value: "",
    },
  ],
  init() {
    this.initSlides();
    this.initSlider();
  },
  initSlides() {
    this.slider = $("._promo__slider");

    this.banners.forEach((el) => {
      $(this.slider).append(this.createSliderItem(el));
    });
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
  createSliderItem(el) {
    const item = document.createElement("div");
    item.classList.add("promo__slider-item");
    const img = document.createElement("img");
    img.style.setProperty(
      "--m-image",
      `url(../img/promo/mobile/${el.img})`,
      ""
    );
    img.style.setProperty(
      "--t-image",
      `url(../img/promo/tablet/${el.img})`,
      ""
    );
    item.append(img)

    return item;
  },
};
