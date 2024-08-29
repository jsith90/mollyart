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
