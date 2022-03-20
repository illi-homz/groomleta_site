grummer.popupFeedback = {
  open() {
    this.$popupMain = $("._popup-feedback");
    grummer.popup.open(this.$popupMain);
  },
  async submit(form, event) {
    event.preventDefault();

    const validator = new Validator(form);
    const v = validator.validate();
    if (!v) return;

    const msg =
      "*Отзыв*\n\n" +
      `#Клиент: ${form.name.value} ${form.lastname.value}\n` +
      `#Комментарий: ${form.comment.value}`;

    const res = await grummer.tlg.sendMessage(msg);

    if (res)
      setTimeout(() => {
        // console.log(res);
        form.reset();

        grummer.popup.open("_popup-ok");
      }, 300);
  },

  changeCounter(fieldInput) {
    const textLength = fieldInput.value.length;
    $(fieldInput)
      .parent("._field")
      .siblings("._popup-main__form-field-counter")
      .find("span")
      .html(textLength);
  },
};
