// garyFunnel 0.1.1
class GaryFunnel {
  constructor() {
    this.pageUrl = window.location.href;
    // this.initializeFoundation();
    this.bindEvents();
  }

  initializeFoundation() {
    // include foundation JS features in the future.
    $(document).foundation();
  }

  bindEvents() {
    $(".menu-wrapper").on("click", this.toggleMenu.bind(this));
    $(".nextPanel").on("click", this.showSecondPart.bind(this));
    $(".goBack").click(this.showFirstPart.bind(this));
    $(".sendData").click((e) => this.validateAndSendData(e));
    $(".menu-toggle").click(this.toggleMenuVisibility.bind(this));
    $(".privacyPolicyButton").click(this.showPrivacyPolicy.bind(this));
    $(".privacyPolicyCloseButton").click(this.hidePrivacyPolicy.bind(this));
    document.addEventListener(
      "DOMContentLoaded",
      this.initializeLazyLoading.bind(this)
    );
  }

  toggleMenu() {
    var menuBtn = ".menu-btn";
    var menuBtnOn = "menu-btn-on";
    var menuWrapOn = "menu-wrapper-on";
    $(this).toggleClass(menuWrapOn);
    $(menuBtn).toggleClass(menuBtnOn);
  }

  showPrivacyPolicy(e) {
    e.preventDefault();
    $(".privacyPolicy").show().addClass("active");
  }

  hidePrivacyPolicy(e) {
    e.preventDefault();
    $(".privacyPolicy").hide().removeClass("active");
  }

  showSecondPart(e) {
    e.preventDefault();
    $("#firstPart").hide();
    $("#secondPart").show();
  }

  showFirstPart() {
    $("#secondPart").hide();
    $("#firstPart").show();
  }

  async validateAndSendData(e) {
    e.preventDefault();
    let formData = this.collectFormData();
    if (this.isFormDataValid(formData)) {
      $("#loader-wrapper").show();
      try {
        this.sendFormData({ ...formData, pageUrl: this.pageUrl }, function () {
          $("#loader-wrapper").hide();
        });
      } catch (error) {
        alert("Failed to fetch IP information. Please try again.");
        $("#loader-wrapper").hide();
      }
    } else {
      alert("Please fill out all required fields.");
    }
  }

  collectFormData() {
    return {
      propertyType: $('select[name="propertyType"]').val(),
      serviceType: $('select[name="serviceType"]').val(),
      urgency: $('select[name="urgency"]').val(),
      name: $('input[name="name"]').val(),
      email: $('input[name="email"]').val(),
      phone: $('input[name="phone"]').val(),
      locAddress: $('input[name="location"]').val(),
      pageTitle: document.title,
    };
  }

  isFormDataValid(formData) {
    return !Object.values(formData).some((value) => !value);
  }

  sendFormData(formData, callback) {
    $.ajax({
      type: "POST",
      url: "contact/app.php",
      data: formData,
      success: function () {
        $(".callout")
          .empty()
          .append(
            "<h2>Thank you for your submission. We will be in touch shortly.</h2>"
          );
        callback();
      },
      error: function () {
        alert("There was an error processing your request. Please try again.");
        callback();
      },
    });
  }

  toggleMenuVisibility() {
    $(".menu").toggle();
  }

  initializeLazyLoading() {
    const lazyImages = [].slice.call(
      document.querySelectorAll("img.lazy-load")
    );

    if ("IntersectionObserver" in window) {
      let lazyImageObserver = new IntersectionObserver(function (
        entries,
        observer
      ) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            let lazyImage = entry.target;
            lazyImage.src = lazyImage.dataset.src;
            lazyImage.classList.remove("lazy-load");
            lazyImageObserver.unobserve(lazyImage);
          }
        });
      });

      lazyImages.forEach(function (lazyImage) {
        lazyImageObserver.observe(lazyImage);
      });
    } else {
      lazyImages.forEach(function (lazyImage) {
        lazyImage.src = lazyImage.dataset.src;
        lazyImage.classList.remove("lazy-load");
      });
    }
  }
}

$(document).ready(function () {
  new GaryFunnel();
  var headerVisible = true;
  function hideHeader() {
    if (headerVisible) {
      $(".top-bar").addClass("super-hide");
      headerVisible = false;
    }
  }
  function attemptHideHeader(timer = 2000) {
    setTimeout(hideHeader, timer);
  }
  attemptHideHeader();
  $(window).scroll(function () {
    if ($(this).scrollTop() === 0) {
      if (!headerVisible) {
        $(".top-bar").removeClass("super-hide");
        headerVisible = true;
        attemptHideHeader(5000);
      }
    }
  });
});
