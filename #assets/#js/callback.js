grummer.callback = {
  init()
  {
    $("._input-phone").mask("+7(999)999-99-99");
  },
  async submit(form, event)
  {
    event.preventDefault();

    const validator = new Validator(form)

    const v = validator.validate()

    if(!v) return

    const res = await grummer.tlg.sendCallBack(form)
    console.log(res);

    if (res) setTimeout(() => {
      grummer.popup.open('_popup-ok')
      form.reset()
    }, 100)
  }
}
