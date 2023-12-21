const increaseButtons = document.querySelectorAll(".increase-quantity");
const decreaseButtons = document.querySelectorAll(".decrease-quantity");
const quantityElements = document.querySelectorAll(".item-quantity");
const priceElements = document.querySelectorAll(".cart-item-price");
const totalPriceElement = document.getElementById("total-price");

updateTotalPrice();

increaseButtons.forEach((button, index) => {
    button.addEventListener("click", (event) => {
        event.preventDefault();
        const currentItem = event.target.closest(".cart-item");
        const quantityElement = currentItem.querySelector(".item-quantity");
        const priceElement = currentItem.querySelector(".cart-item-price");
        const pricePerItem = parseFloat(priceElement.getAttribute("data-price"));
        const currentQuantity = parseInt(quantityElement.textContent);

        quantityElement.textContent = currentQuantity + 1;
        updateCartItemPrice(priceElement, pricePerItem, currentQuantity + 1);
        
        // Call updateTotalPrice after modifying the quantity
        updateTotalPrice();
        console.log(updateTotalPrice())
    });
});

decreaseButtons.forEach((button, index) => {
    button.addEventListener("click", (event) => {
        event.preventDefault();
        const currentItem = event.target.closest(".cart-item");
        const quantityElement = currentItem.querySelector(".item-quantity");
        const priceElement = currentItem.querySelector(".cart-item-price");
        const pricePerItem = parseFloat(priceElement.getAttribute("data-price"));
        const currentQuantity = parseInt(quantityElement.textContent);

        if (currentQuantity > 1) {
            quantityElement.textContent = currentQuantity - 1;
            updateCartItemPrice(priceElement, pricePerItem, currentQuantity - 1);

            // Call updateTotalPrice after modifying the quantity
            updateTotalPrice();
            console.log(updateTotalPrice())
        }
    });
});

function updateCartItemPrice(priceElement, pricePerItem, quantity) {
    const totalPrice = (pricePerItem * quantity).toFixed(2);
    priceElement.textContent = "₱" + totalPrice;
}

function updateTotalPrice() {
    // Check if totalPriceElement exists
    if (!totalPriceElement) {
        console.error("Total price element not found");
        return;  // Exit the function if the element is not found
    }

    let totalPrice = 0;

    // Calculate the total price by summing up the individual item prices
    priceElements.forEach(function (priceElement) {
        const quantityElement = priceElement.previousElementSibling;

        if (quantityElement) {
            const quantity = parseInt(quantityElement.textContent);
            const price = parseFloat(priceElement.getAttribute('data-price'));

            if (!isNaN(quantity) && !isNaN(price)) {
                totalPrice += price * quantity;
            } else {
                console.error("Invalid quantity or price:", quantity, price);
            }
        } else {
            console.error("Quantity element not found:", priceElement);
        }
    });

    // Update the total price element
    totalPriceElement.textContent = "₱" + totalPrice.toFixed(2);
}

console.log(totalPriceElement)