grummer.questions = {
  init()
  {
    this.$spoiler = $('.questions__spoiler')
    this.items = this.$spoiler.find('.questions__item')
  },
  toggleText(el)
  {
    const $el = $(el)
    const $parent = $el.parent('.questions__item')
    const $text = $el.siblings('.questions__item-text')

    $parent.hasClass('active')
      ? this.slideUp($parent, $text)
      : this.slideDown($parent, $text)
  },
  slideUp($parent, $text)
  {
    $parent.removeClass('active')
    $text.slideUp(300)
  },
  slideDown($parent, $text)
  {
    this.items
      .removeClass('active')
      .find('.questions__item-text')
      .slideUp(300)
    $parent.addClass('active')
    $text.slideDown(300)
  },
}
