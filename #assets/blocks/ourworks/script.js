grummer.ourworks = {
	init() {
	  this.nav = $(".ourworks__nav");
	  this.title = $(".ourworks__title");
	  this.text = $(".ourworks__text");
	  this.slider = null;
	  this.initSlider();
	},
	initSlider() {
	  this.slider = $("._ourworks__slider");

	  if (!this.slider.length) {
		  return
	  }
  
	  const slickParams = {
		mobileFirst: true,
		infinite: true,
		dots: true,
		centerMode: true,
		slidesToShow: 1,
		slidesToScroll: 1,
		prevArrow: `<div class="prev-arrow slider-arrow">${arrow}</div>`,
		nextArrow: `<div class="next-arrow slider-arrow">${arrow}</div>`,
		responsive: [
		  {
			breakpoint: 768,
			settings: {
			  variableWidth: true,
			},
		  },
		],
	  };
  
	  this.slider.slick(slickParams);
  
	  this.slider.on("setPosition", () => this.moveArrows(false));
  
	  this.moveArrows(true)
	},
	moveArrows(isInit) {
	  isInit && $("._ourworks__slider").slick("slickGoTo", 0);
  
	  if (window.innerWidth < 1024) {
		$(".ourworks .prev-arrow").css("left", 12);
		$(".ourworks .next-arrow").css("right", 12);
  
		return;
	  }
  
	  setTimeout(() => {
		const CurrentSlide = $(".ourworks .slick-current.slick-center").get(0);
		const slideData = CurrentSlide.getBoundingClientRect();
  
		$(".ourworks .prev-arrow").css("left", slideData.left - 25);
		$(".ourworks .next-arrow").css(
		  "right",
		  slideData.right - slideData.width - 25
		);
	  }, 0);
	},
  };
  