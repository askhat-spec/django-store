$(".products").owlCarousel({
  autoplay: true,
  autoplayhoverpause: true,
  autoplaytimeout: 65,
  items: 4,
  nav: true,
  loop: true,
  dots: false,
  stagePadding: 20,
  responsive: {
    0: {
      items: 1,
    },
    728: {
      items: 2,
    },
    960: {
      items: 3,
    },
    1200: {
      items: 4,
    },
  },
});

$(".header-carousel").owlCarousel({
  loop: true,
  autoplay: true,
  margin: 30,
  animateOut: "fadeOut",
  animateIn: "fadeIn",
  dots: true,
  autoplayHoverPause: false,
  items: 1,
  responsive: {
    0: {
      items: 1,
    },
    600: {
      items: 1,
    },
    1000: {
      items: 1,
    },
  },
});
