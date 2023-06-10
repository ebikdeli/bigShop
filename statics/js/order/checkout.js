// * Calculate order tax
let orderPrice = Number(document.getElementById('order-payment-price').innerText);
let orderTax = document.getElementById('order-payment-tax');

orderTax.innerText = (orderPrice * 0.09).toFixed(0);


// * Calculate order total price
var orderShipmentCost = Number(document.getElementById('order-shipment-cost').innerText);
var totalPrice = orderPrice + Number(orderTax.innerText) + orderShipmentCost;
document.getElementById('order-payment-total').innerText = totalPrice.toFixed(0);