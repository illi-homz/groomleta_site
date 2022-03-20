'use strict';

grummer.header = {
  init() {
    this.dataInit()
    this.linksTemplating(this.navList)
    this.linksTemplating(this.mobileMenuLinks)
    this.changeBg()
  },
  dataInit() {
    this.backgrounds = ['1_dog.jpg', '2_cat.jpg', '3_dog.jpg', '4_cat.jpg']
    this.headerBg = $('div.header__bg')
    this.links = [
      {title: 'О салоне', value: 'about'},
      {title: 'Услуги', value: 'services'},
      {title: 'Наши работы', value: 'ourworks'},
      {title: 'Акции', value: 'promo'},
      {title: 'Отзывы', value: 'feedbacks'},
      {title: 'Контакты', value: 'footer'}
    ]
    this.navList = $('.header__links')
    this.mobileMenuLinks = $('.header__mobile-menu-links')
    this.linksTemplate = $.trim( $('#header__links').html() )
    this.menu = $('.header__mobile-menu')
    this.burger = $('.header__burger')
  },
  changeBg() {
    let count = 1
    const timeFade = 1000
    const timeChange = 9000
    const arrLen = this.backgrounds.length

    return setInterval(() => {
      if ( count > arrLen - 1 ) count = 0
      this.headerBg.fadeOut(timeFade, () => {
        this.headerBg.css({background: `url(img/main/${this.backgrounds[count]}) bottom / cover no-repeat`})
        this.headerBg.fadeIn(timeFade)
        count++
      })
    }, timeChange)
  },
  linksTemplating( list ) {
    const isMobile = list.hasClass( 'header__mobile-menu-links' )

    let frag = ''
    $.each( this.links, ( index, obj ) => {
      frag += this.linksTemplate
        .replace( /{{title}}/ig, obj.title )
        .replace( /{{value}}/ig, obj.value )
        .replace( /{{isMobile}}/ig, isMobile )
    })
    list.append(frag)
  },
  toggleMenu() {
    this.menu.slideToggle( 300 )
    this.burger.toggleClass('active')

    $('body').css('overflow') === 'visible'
      ? $('body').css({overflow: 'hidden'})
      : $('body').css({overflow: 'auto'})
  }
}
