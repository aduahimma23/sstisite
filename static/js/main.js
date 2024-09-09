(function ($) {
    "use strict";
    
    // Dropdown on mouse hover
    $(document).ready(function () {
        function toggleNavbarMethod() {
            if ($(window).width() > 992) {
                $('.navbar .dropdown').on('mouseover', function () {
                    $('.dropdown-toggle', this).trigger('click');
                }).on('mouseout', function () {
                    $('.dropdown-toggle', this).trigger('click').blur();
                });
            } else {
                $('.navbar .dropdown').off('mouseover').off('mouseout');
            }
        }
        toggleNavbarMethod();
        $(window).resize(toggleNavbarMethod);
    });
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });
    
})(jQuery);

document.addEventListener('DOMContentLoaded', function () {
    const wrapper = document.querySelector('.testimonial-wrapper');
    const items = document.querySelectorAll('.testimonial-item');
    const itemCount = items.length;
    let currentIndex = 0;

    function showNextTestimonials() {
        currentIndex += 3;
        if (currentIndex >= itemCount) {
            currentIndex = 0;
        }
        wrapper.style.transform = `translateX(-${currentIndex * 33.33}%)`;
    }

    setInterval(showNextTestimonials, 5000);
});