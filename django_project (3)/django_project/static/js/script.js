let subMenu = document.getElementById("profile-subMenu")

function toggleMenu() {
    subMenu.classList.toggle("open-menu")
}

function updateCartCount() {
    var cartCount = document.querySelector('.cart-count');
    fetch('{% url "fetch-cart-count" %}')
        .then(response => response.json())
        .then(data => {
            cartCount.textContent = data.cart_count;
        });
}

updateCartCount();