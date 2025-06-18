// intialization plugins
$(document).ready(function () {

    //animation icon toggler of navbar
    $(`.navbar-toggler`).click(function() {
        $(`.navbar-toggler`).toggleClass(`active`);
    });

    //Wow intit
    wow = new WOW({
        boxClass: 'wow',
        animateClass: 'animated',
        offset: 200,
        mobile: true,
        live: false
    });
    wow.init();

    //fancybox
    $("[data-fancybox]").fancybox({
        selector: '[data-fancybox="images"]',
        // loop: true
    });

    //  loader 
    // $(window).on("load", function() {
    //     $("#preloader").addClass("isdone");
    // });

});

// Swiper
$(document).ready(function () {

    //////////////////// feedback_swiper  ////////////////////
    var swiper = new Swiper('.feedback_sec .feedback_swiper', {
        loop: true,
        speed: 900,
        slidesPerView: 1.8,
        spaceBetween: 175,
        centeredSlides: true,
        autoplay: {
            delay: 3000,
        },
        navigation: {
            nextEl: '.feedback_sec .swiper-button-next',
            prevEl: '.feedback_sec .swiper-button-prev',
        },
        pagination: {
            el: '.feedback_sec .swiper-pagination',
            clickable: true
        },
        breakpoints: {
            0: {
                slidesPerView: 1,
                spaceBetween: 20,
            },
            768: {
                slidesPerView: 1.2,
                spaceBetween: 20,
            },
            1024: {
                slidesPerView: 1.8,
                spaceBetween: 175,
                // Prevent swiper in lg screens
                // allowTouchMove: false,
                // preventClicks: false
            },
        }
    });

    //////////////////// Swiper  ////////////////////
    // var swiper = new Swiper(' .swiper-container', {
    //     // loop: true,
    //     speed: 900,
    //     slidesPerView: 1,
    //     spaceBetween: 15,
    //     // autoplay: {
    //     //     delay: 2500,
    //     // },
    //     //In Tabs
    //     // observer: true,
    //     // observeParents: true,
    //     navigation: {
    //         nextEl: '.swiper-button-next',
    //         prevEl: '.swiper-button-prev',
    //     },
    //     pagination: {
    //         el: '.swiper-pagination',
    //         clickable: true
    //     },
    //     breakpoints: {
    //         640: {
    //             slidesPerView: 2,
    //             spaceBetween: 20,
    //         },
    //         768: {
    //             slidesPerView: 3,
    //             spaceBetween: 20,
    //         },
    //         1024: {
    //             slidesPerView: 5,
    //             spaceBetween: 20,
    //             // Prevent swiper in lg screens
    //             // allowTouchMove: false,
    //             // preventClicks: false
    //         },
    //     }
    // });

});


