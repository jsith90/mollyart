function commissionSlides() {
    // Get the modal
    const modal = document.getElementById("myModal");
    if (modal) {

        // Get the modal image and caption elements
        const modalImg = document.getElementById("img01");

        // Get all images that will open the modal
        const images = document.querySelectorAll('.modal-img');

        // Add click event listeners to each image
        images.forEach((img, index) => {
          img.onclick = function() {
            modal.style.display = "block";
            modal.style.zIndex = "1000";
            slideIndex = index + 1;  // Update the slide index
            showSlides(slideIndex);
          }
        });

        // Get the <span> element that closes the modal
        const span = document.getElementsByClassName("close")[0];

        // When the user clicks on <span> (x), close the modal
        span.onclick = function() {
          modal.style.display = "none";
        };

        let slideIndex = 1;

        // Next/previous controls
        function plusSlides(n) {
          showSlides(slideIndex += n);
        }

        // Thumbnail image controls
        function currentSlide(n) {
          showSlides(slideIndex = n);
        }

        function showSlides(n) {
          const images = document.querySelectorAll('.modal-img');  // Get all the images again
          const dots = document.getElementsByClassName("demo");

          if (n > images.length) { slideIndex = 1 }
          if (n < 1) { slideIndex = images.length }

          // Update the modal image and caption
          modalImg.src = images[slideIndex - 1].src;
          captionText.innerHTML = images[slideIndex - 1].alt;

          // Remove 'active' class from all dots
          for (let i = 0; i < dots.length; i++) {
            dots[i].className = dots[i].className.replace(" active", "");
          }

          // Add 'active' class to the corresponding dot
          dots[slideIndex - 1].className += " active";
        }
    } else {
        console.log('no modal.');
    }
}

function navScroll() {
    // Select the .hatman-div element and nav
    const hatmanDiv = document.querySelector('.hatman-div');
    const nav = document.getElementsByTagName('nav')[0];
    const logo = document.querySelector('.logo-div'); 
    const logoName = document.getElementById('logo-name');
    const logoMan = document.getElementById('logo-man');
    const landing = document.querySelector('.landing');
    const hatmanImage = document.querySelector('.hatman-image');
    const croeso = document.querySelector('.croeso');
    const reviews = document.querySelector('.slideshow');
    const home = document.querySelector('.home');
    const wave = document.querySelector('.svg-wave-over');
    const wave2 = document.querySelector('.svg-wave-over-home')
    const footer = document.getElementsByTagName('footer')[0];
    const landingIcons = document.querySelector('.landing-icons');
    const navToggleOpen = document.querySelector(".nav-toggle-open");
    const navToggleClose = document.querySelector(".nav-toggle-close");

    let lastScrollY = window.scrollY; // To keep track of the last scroll position
    let navHeight = nav.offsetHeight;

    if (hatmanDiv) {
        wave.style.display = "none";
        footer.style.display = "none";
        home.style.minHeight = "100vh";
        function handleScroll() {
            const currentScrollY = window.scrollY;

            if (currentScrollY > navHeight) {
                // Scrolling down: add classes
                hatmanDiv.classList.add('hatman-scroll');
                logoName.classList.add('nav-scroll');
                landing.classList.add('landing-scroll');
                reviews.classList.add('see-reviews');
                landingIcons.classList.add('landing-scroll');
                landingIcons.style.height = "100vh";
                hatmanImage.style.animationName = 'none';
                home.style.minHeight = "auto";
                logoMan.classList.add('man-appear');
                wave2.classList.add('wave-appear');
                if (window.innerWidth > 1060) {
                    croeso.style.width = "30%";
                } else {
                    croeso.style.width = "70%";
                }
                // home.style.background = "#e7e5d5";
            } else {
                // Scrolling up: remove classes
                // hatmanDiv.classList.remove('hatman-scroll');
                // nav.classList.remove('nav-scroll');
                // landing.classList.remove('landing-scroll');
                console.log("hatman is in the nav.");
            }

            // Update the last scroll position
            lastScrollY = currentScrollY;
        }

        // Add scroll event listener
        window.addEventListener('scroll', handleScroll);
    
    } else {
        console.log("The .hatman-div does not exist on this page.");
    }

    navToggleOpen.addEventListener("click", function () {
        wave[0].style.display = "none";
        hatmanDiv.style.display = "none";
    });

    navToggleClose.addEventListener("click", function () {
        wave[0].style.display = "block";
        hatmanDiv.style.display = "flex";
    });

    if (reviews) {

        // set index and transition delay
        let index = 0;
        let transitionDelay = 10000;

        // get div containing the slides
        let slideContainer = document.querySelector(".slideshow");
        // get the slides
        let slides = slideContainer.querySelectorAll(".slide");

        // set transition delay for slides
        for (let slide of slides) {
          slide.style.transition = `opacity 2s ease-in-out`;
        }

        // show the first slide
        showSlide(index);

        // show a specific slide
        function showSlide(slideNumber) {
            slides.forEach((slide, i) => {
            slide.style.opacity = i == slideNumber ? "1" : "0";
            });
            // next index
            index++;
            // go back to 0 if at the end of slides
            if (index >= slides.length) {
                index = 0;
            }
        }

        // transition to next slide every x seconds
        setInterval (() => showSlide(index), transitionDelay);
    } else {
        console.log('no reviews here.');
    }
}

function navBar() {
    const toggleDiv = document.querySelector(".toggle-div");
    const navToggleOpen = document.querySelector(".nav-toggle-open");
    const navToggleClose = document.querySelector(".nav-toggle-close");
    const links = document.querySelector(".nav-options");
    const navName = document.getElementById("logo-name");
    const navMan = document.getElementById("logo-man");
    const nav = document.getElementsByTagName("nav")[0]; 


    navToggleOpen.addEventListener("click", function () {
        // console.log(links.classList);
        // console.log(links.classList.contains("random"));
        // console.log(links.classList.contains("links"));
        // if (links.classList.contains("show-links")) {
        //   links.classList.remove("show-links");
        // } else {
        //   links.classList.add("show-links");
        // }
        links.classList.add("show-options");
        navToggleOpen.style.opacity = "0";
        navToggleClose.style.opacity = "1";
        navToggleOpen.style.zIndex = "0";
        navToggleClose.style.zIndex = "1";
        nav.style.marginBottom = "0";
    });

    navToggleClose.addEventListener("click", function () {
        // console.log(links.classList);
        // console.log(links.classList.contains("random"));
        // console.log(links.classList.contains("links"));
        // if (links.classList.contains("show-links")) {
        //   links.classList.remove("show-links");
        // } else {
        //   links.classList.add("show-links");
        // }
        links.classList.remove("show-options");
        navToggleOpen.style.opacity = "1";
        navToggleClose.style.opacity = "0";
        navToggleOpen.style.zIndex = "1";
        navToggleClose.style.zIndex = "0";
        nav.style.marginBottom = "2rem";
    });
}

function initShopItemEvents() {
    const shopItem = document.querySelectorAll('.shop-item');
    
    if (shopItem.length > 0) {
        shopItem.forEach((item, index) => {
            item.onmouseover = function() {
                shopItem[index].style.cursor = "pointer"; 
                const shopBadge = item.querySelectorAll('.view-product-sold, .view-product-sale, .view-product-available');
                const shopText = item.querySelectorAll('.item-detail > h3, .item-detail > p, .item-detail > h4');
                const shopImage = item.querySelectorAll('.modal-img');
                shopText.forEach(text => {
                    text.style.color = "#0065d9";
                });
                shopBadge.forEach(badge => {
                    badge.style.background = "#0065d9";
                    badge.style.border = "#0065d9";
                    badge.style.boxShadow = "black 6px 6px 1px 1px";
                });
                shopImage.forEach(image => {
                    image.style.opacity = "0.7";
                });
            };

            item.onmouseout = function() {
                shopItem[index].style.cursor = "revert";
                const saleBadge = item.querySelectorAll('.view-product-sale');
                const soldBadge = item.querySelectorAll('.view-product-sold');
                const availableBadge = item.querySelectorAll('.view-product-available');
                const shopText = item.querySelectorAll('.item-detail > h3, .item-detail > p, .item-detail > h4');
                const shopImage = item.querySelectorAll('.modal-img');
                shopText.forEach(text => {
                    text.style.color = "black";
                });
                saleBadge.forEach(badge => {
                    badge.style.background = "red";
                    badge.style.border = "red";
                    badge.style.boxShadow = "none";
                });
                soldBadge.forEach(badge => {
                    badge.style.background = "black";
                    badge.style.border = "black";
                    badge.style.boxShadow = "none";
                });
                availableBadge.forEach(badge => {
                    badge.style.background = "#3f9c44";
                    badge.style.border = "#3f9c44";
                    badge.style.boxShadow = "none";
                });
                shopImage.forEach(image => {
                    image.style.opacity = "1";
                });
            };
        });
    }
}

function initCheckoutButton() {
    const checkout = document.getElementById('checkout');
    
    if (checkout) {
        checkout.addEventListener('mouseover', function() {
            checkout.style.cursor = "pointer"; 
            checkout.style.background = "#0065d9";
            checkout.style.border = "#0065d9";
            checkout.style.boxShadow = "black 6px 6px 1px 1px";
        });

        checkout.addEventListener('mouseout', function() {
            checkout.style.background = "#3f9c44";
            checkout.style.border = "#3f9c44";
            checkout.style.boxShadow = "none";
        });
    }
}

function togglePaymentPageInfo() {
    // Select all elements with the class 'summary-toggle'
    const summaryToggles = document.querySelectorAll(".summary-toggle");
    const paymentDisplay = document.querySelector('.payment-display');
    const footer = document.getElementsByTagName('footer')[0];
    if (paymentDisplay) {
        footer.style.display = "none";
    } else {
        console.log('no checkout')
    }
    
    summaryToggles.forEach((toggle) => {
        toggle.addEventListener("mouseover", function() {
            
            // const shopText = item.querySelectorAll('.item-detail > h3, .item-detail > p, .item-detail > h4');
            toggle.style.cursor = "pointer";
            toggle.style.background = "#0065d9";
        });

        toggle.addEventListener("mouseout", function() {
            toggle.style.background = ""; // Reset background on mouse out
        });
        // Add click event listener to each summary-toggle
        toggle.addEventListener("click", function () {
            // Find the next sibling element with the class 'payment-detail'
            const paymentDetail = this.nextElementSibling;
            
            // Toggle the 'payment-detail-display' class to show/hide the details
            if (paymentDetail) {
                paymentDetail.classList.toggle("payment-detail-display");
            }
        });
    });
}

// Move the functions outside to make them globally accessible
let slideIndex = 1;
const modalImg = document.getElementById("img01");

function plusSlides(n) {
    showSlides(slideIndex += n);
}

function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    const images = document.querySelectorAll('.modal-img');
    const dots = document.getElementsByClassName("demo");

    if (n > images.length) { slideIndex = 1 }
    if (n < 1) { slideIndex = images.length }

    // Update the modal image and caption
    modalImg.src = images[slideIndex - 1].src;
    captionText.innerHTML = images[slideIndex - 1].alt;

    // Remove 'active' class from all dots
    for (let i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }

    // Add 'active' class to the corresponding dot
    dots[slideIndex - 1].className += " active";
}


function initModal() {
    const modal = document.getElementById("myModal");
    const images = document.querySelectorAll('.modal-img');
    const span = document.getElementsByClassName("close")[0];

    if (images.length > 0 && modal && modalImg) {
        images.forEach((img, index) => {
            img.onclick = function() {
                modal.style.display = "block";
                modal.style.zIndex = "1000";
                slideIndex = index + 1;
                showSlides(slideIndex);
            };
        });
    }

    if (span) {
        span.onclick = function() {
            modal.style.display = "none";
        };
    }
}

function trolleyPage() {
    const checkoutProduct = document.querySelector('.checkout-product');
    const footer = document.getElementsByTagName('footer')[0];
    if (checkoutProduct) {
        footer.style.display = "none";
    } else {
        console.log('no checkout')
    }
}

function checkoutPages() {
    const orderDisplay = document.querySelector('.order-display');
    const footer = document.getElementsByTagName('footer')[0];
    if (orderDisplay) {
        footer.style.display = "none";
    } else {
        console.log('no checkout')
    }
}

// Call these functions to initialize events based on the template
initShopItemEvents();
initCheckoutButton();
initModal();
togglePaymentPageInfo();
navBar();
navScroll();
trolleyPage(); 
checkoutPages();
commissionSlides();