function navScroll() {
    // Select the .hatman-div element and nav
    const hatmanDiv = document.querySelector('.hatman-div');
    // const nav = document.getElementsByTagName('nav')[0];
    const logo = document.querySelector('.logo-div'); 
    const logoName = document.getElementById('logo-name');
    const logoMan = document.getElementById('logo-man');
    const landing = document.querySelector('.landing');
    const hatmanImage = document.querySelector('.hatman-image');
    const commission = document.getElementById('commission');
    const shop = document.getElementById('shop');
    const portfolio = document.getElementById('portfolio');


    let lastScrollY = window.scrollY; // To keep track of the last scroll position

    if (hatmanDiv) {
        function handleScroll() {
            const currentScrollY = window.scrollY;

            if (currentScrollY > lastScrollY) {
                // Scrolling down: add classes
                hatmanDiv.classList.add('hatman-scroll');
                logoName.classList.add('nav-scroll');
                landing.classList.add('landing-scroll');
                hatmanImage.style.animationName = 'none';
                logoMan.classList.add('man-appear');
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

    commission.addEventListener("mouseover", function () {
        commission.classList.add("no-bounce");
    });

    commission.addEventListener("mouseout", function () {
        commission.classList.remove("no-bounce");
    });

    shop.addEventListener("mouseover", function () {
        shop.classList.add("no-bounce");
    });

    shop.addEventListener("mouseout", function () {
        shop.classList.remove("no-bounce");
    });

    portfolio.addEventListener("mouseover", function () {
        portfolio.classList.add("no-bounce");
    });

    shop.addEventListener("mouseout", function () {
        portfolio.classList.remove("no-bounce");
    });

    shop.addEventListener("click", function () {
        shop.classList.add("man-clicked");
    });
}

function navBar() {
    const toggleDiv = document.querySelector(".toggle-div");
    const navToggleOpen = document.querySelector(".nav-toggle-open");
    const navToggleClose = document.querySelector(".nav-toggle-close");
    const links = document.querySelector(".nav-options");
    const navName = document.getElementById("logo-name");
    const navMan = document.getElementById("logo-man");


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
                    text.style.color = "#4eb2ff";
                });
                shopBadge.forEach(badge => {
                    badge.style.background = "#4eb2ff";
                    badge.style.border = "#4eb2ff";
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
                });
                soldBadge.forEach(badge => {
                    badge.style.background = "black";
                    badge.style.border = "black";
                });
                availableBadge.forEach(badge => {
                    badge.style.background = "#3f9c44";
                    badge.style.border = "#3f9c44";
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
            checkout.style.background = "#4eb2ff";
            checkout.style.border = "#4eb2ff";
        });

        checkout.addEventListener('mouseout', function() {
            checkout.style.background = "#3f9c44";
            checkout.style.border = "#3f9c44";
        });
    }
}

function togglePaymentPageInfo() {
    // Select all elements with the class 'summary-toggle'
    const summaryToggles = document.querySelectorAll(".summary-toggle");
    
    summaryToggles.forEach((toggle) => {
        toggle.addEventListener("mouseover", function() {
            
            // const shopText = item.querySelectorAll('.item-detail > h3, .item-detail > p, .item-detail > h4');
            toggle.style.cursor = "pointer";
            toggle.style.background = "#4eb2ff";
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

// Call these functions to initialize events based on the template
initShopItemEvents();
initCheckoutButton();
initModal();
togglePaymentPageInfo();
navBar();
navScroll(); 