const shopItem = document.querySelectorAll('.shop-item');
const checkout = document.querySelectorAll('.checking-out')


shopItem.forEach((item, index) => {
    item.onmouseover = function() {
    	shopItem[index].style.cursor = "pointer"; 
        const shopBadge = item.querySelectorAll('.view-product-sold, .view-product-sale, .view-product-available');
        const shopText = item.querySelectorAll('.item-detail > h3, .item-detail > p, .item-detail > h4');
        shopText.forEach(text => {
        	text.style.color = "#4eb2ff";
        });
        shopBadge.forEach(badge => {
        	badge.style.background = "#4eb2ff";
        	badge.style.border = "#4eb2ff";
        });
    };
});


shopItem.forEach((item, index) => {
	item.onmouseout = function() {
		shopItem[index].style.cursor = "revert";
		const saleBadge = item.querySelectorAll('.view-product-sale');
		const soldBadge = item.querySelectorAll('.view-product-sold');
		const availableBadge = item.querySelectorAll('.view-product-available');
		const shopText = item.querySelectorAll('.item-detail > h3, .item-detail > p, .item-detail > h4');
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
	};
});

checkout.forEach((item, index) => {
    item.onmouseover = function() {
        checkout[index].style.cursor = "pointer"; 
        const shopBadge = item.querySelectorAll('.view-product-available');
        shopBadge.forEach(badge => {
            badge.style.background = "#4eb2ff";
            badge.style.border = "#4eb2ff";
        });
    };
});

checkout.forEach((item, index) => {
    item.onmouseout = function() {
        checkout[index].style.cursor = "pointer"; 
        const shopBadge = item.querySelectorAll('.view-product-available');
        shopBadge.forEach(badge => {
            badge.style.background = "#3f9c44";
            badge.style.border = "#3f9c44";
        });
    };
});