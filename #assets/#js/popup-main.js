const svg = (path) => `
  <svg
    width="6"
    height="12"
    viewBox="0 0 8 14"
    xmlns="http://www.w3.org/2000/svg">
    <path
      d="${path}"
      stroke="#ECEFEF"
      stroke-linecap="round"
      stroke-linejoin="round"></path>
  </svg>
`;

grummer.popupMain = {
  images: [],

  init() {
    new AirDatepicker("#datepicker", {
      dateFormat: (date) => date.toLocaleDateString(),
      prevHtml: svg("M7.04199 12.8713L1.04199 6.87134L7.04199 0.871338"),
      nextHtml: svg("M1 12.8713L7 6.87134L1 0.871338"),
      navTitles: {
        days: "MMMM yyyy",
      },
      minDate: new Date(),
      position({ $datepicker, $target, $pointer }) {
        const coords = $target.getBoundingClientRect()
        const top = coords.y + coords.height + window.scrollY + 4
        const left = coords.x;

        $datepicker.style.left = `${left}px`;
        $datepicker.style.top = `${top}px`;
        $datepicker.style.width = `${coords.width}px`;

        $pointer.style.display = "none";
      },
    });
  },

  open() {
    this.init();

    this.$popupMain = $("._popup-main");
    this.$services = this.$popupMain.find(".popup-main__form-services");
    this.$servicesUl = this.$popupMain.find(".popup-main__form-services-ul");

    const html = this.createServicesListHtml();

    this.$servicesUl.html(html);

    grummer.currentServices.length > 1
      ? this.$services.removeClass("one")
      : this.$services.addClass("one");

    this.setFinalPrice(this.calculateFinalPrice());

    grummer.popup.open(this.$popupMain);
  },
  createServicesListHtml() {
    const template = $.trim($("#popup-main__form-services").html());

    return grummer.currentServices.reduce((acc, service) => {
      return (acc += template
        .replace(/{{id}}/gi, service.id)
        .replace(/{{img}}/gi, service.img)
        .replace(/{{title}}/gi, service.title)
        .replace(/{{price}}/gi, service.price));
    }, "");
  },
  calculateFinalPrice() {
    return grummer.currentServices.reduce((acc, el) => {
      return el.price.includes("-")
        ? (acc += +el.price.split("-")[0])
        : el.price.includes("от")
        ? (acc += +el.price.replace("от", ""))
        : (acc += +el.price);
    }, 0);
  },
  setFinalPrice(price) {
    this.$popupMain.find("._final-price").html(price);
    this.$popupMain.find("input#_final-price").val(price);
  },
  removeService(id) {
    // because popup click outside....
    setTimeout(() => {
      grummer.currentServices = grummer.currentServices.filter((el) => {
        return el.id !== id;
      });

      if (grummer.currentServices.length === 1) this.$services.addClass("one");

      this.$servicesUl.html(this.createServicesListHtml());

      this.setFinalPrice(this.calculateFinalPrice());
    }, 0);
  },
  createServicesStr(nodeList) {
    return Array.from(nodeList)
      .map((el) => {
        return el.value;
      })
      .join(", ");
  },
  async submit(form, event) {
    event.preventDefault();

    const validator = new Validator(form);
    const v = validator.validate();
    if (!v) return;

    let services;

    form.services instanceof RadioNodeList
      ? (services = this.createServicesStr(form.services))
      : (services = form.services.value);

    const msg =
      "*Запись*\n\n" +
      `#Услуги: ${services}\n` +
      `#Клиент: ${form.name.value} ${form.lastname.value}\n` +
      `#Тел: ${form.tel.value}\n` +
      `#Дата: ${form.date.value}\n` +
      `#Комментарий: ${form.comment.value}\n` +
      `#Мин цена: ${form.price.value}\n`;

    const res = await grummer.tlg.sendMessage(msg);

    const files = Array.from(form.images.files);

    if (files.length) {
      if (files.length === 1) {
        grummer.tlg.sendImg(files[0])
      } else {
        grummer.tlg.sendImgs(files);
      }
    }

    this.removeAllRenderedImages();

    if (res)
      setTimeout(() => {
        form.reset();

        grummer.popup.open("_popup-ok");
      }, 300);
  },

  loadImages() {
    $("#form-animals-imgs").focus().trigger("click");
  },
  onInputClick(el, event) {
    event.stopPropagation();
  },
  onUploadImages(el) {
    const imgs = Array.from(el.files)
      .slice(0, 4 - this.images.length)
      .filter((img) => {
        for (let i = 0; i < this.images.length; i++) {
          if (img.name === this.images[i].name) {
            return false;
          }
        }

        return true;
      });

    if (!imgs.length) return;

    this.images = [...this.images, ...imgs];

    const dt = new DataTransfer();
    imgs.forEach((img) => dt.items.add(img));
    el.files = dt.files;

    this.renderImages(imgs);
  },
  renderImages(files) {
    files.forEach(this.renderImage);
  },
  renderImage(img, idx) {
    const reader = new FileReader();
    const imgNode = document.createElement("img");
    reader.onloadend = () => {
      imgNode.src = reader.result;
    };
    reader.readAsDataURL(img);

    const $imageWrapper = $('<div"></div>')
      .addClass("popup-main__form-image-wrapper")
      .addClass("_popup-main__form-image-wrapper")
      .attr("id", "image-" + idx);
    const $imageRemove = $("<div></div>").addClass(
      "popup-main__form-image-remove"
    );
    $imageRemove.click((e) => grummer.popupMain.removeImage(e, img.name));

    $imageWrapper.append(imgNode);
    $imageWrapper.append($imageRemove);

    $("._popup-main__form-imgs-add").before($imageWrapper);

    $("._popup-main__form-img-loader").addClass("active");
  },
  removeImage(event, name) {
    event.stopPropagation();
    const $input = $("#form-animals-imgs");

    const dt = new DataTransfer();

    this.images = this.images.filter((img) => img.name !== name);
    this.images.forEach((img) => dt.items.add(img));

    $input[0].files = dt.files;

    if (!this.images.length) {
      $("._popup-main__form-img-loader").removeClass("active");
    }

    $(event.target).parent("._popup-main__form-image-wrapper").remove();
  },
  removeAllRenderedImages() {
    $("._popup-main__form-image-wrapper").remove();
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
