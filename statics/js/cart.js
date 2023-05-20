// Base cart template and script:
// https://codepen.io/justinklemm/pen/kyMjjv
import {addOne, minuseOne, checkCartQuantity} from './functions.js';
import {sendPostData} from './ajax.js';


// * When page first load, check if cart is empty or not
let emptyCartElem = document.querySelector('.cart--no--items');
let cartExistElem = document.querySelector('.cart--items-exists');
let totalItemsElem = document.querySelector('#cart-items');
checkCartQuantity(totalItemsElem, emptyCartElem, cartExistElem);


// * Funtions to 'remove', 'update Quantity' and 'reCalculate' items for the cart
/* Set rates + misc */
var taxRate = 0.05;
var shippingRate = 4500; 
var fadeTime = 300;

/* Recalculate cart */
function recalculateCart()
{
  var subtotal = 0;
  let totalQuantity = 0;
  
  /* Sum up row total prices */
  $('.cart--total--price--value').each(function () {
    subtotal += parseFloat($(this).text());
  });
  /* Sum up total quantity */
  Array.from(document.querySelectorAll('.cart--product--quantity')).forEach(inputElem => {
    totalQuantity += Number(inputElem.value);
  })
  
  /* Calculate totals */
  var tax = subtotal * taxRate;
  var shipping = (subtotal > 0 ? shippingRate : 0);
  var total = subtotal + tax + shipping;
  
  /* Update totals display */
  $('.totals-value').fadeOut(fadeTime, function() {
    $('#cart-subtotal').html(subtotal.toFixed(0));
    $('#cart-tax').html(tax.toFixed(0));
    $('#cart-shipping').html(shipping.toFixed(0));
    $('#cart-total').html(total.toFixed(0));
    $('#cart-items').html(totalQuantity.toFixed(0));
    if(total == 0){
      $('.checkout').fadeOut(fadeTime);
    }else{
      $('.checkout').fadeIn(fadeTime);
    }
    $('.totals-value').fadeIn(fadeTime);

    // Check if cart is empty
    checkCartQuantity(totalItemsElem, emptyCartElem, cartExistElem);
  });
}


/* Update quantity */
function updateQuantity(quantityInputElem)
{
  /* Calculate line price */
  var productRow = $(quantityInputElem).parent().parent().parent();
  var price = parseFloat(productRow.children('.cart--unit--price--column').children('.cart--unit--price--box').children('.cart--unit-price--value').text());
  var quantity = $(quantityInputElem).val();
  var linePrice = price * quantity;
  /* Update line price display and recalc cart totals */
  productRow.children('.cart--total--price--column').children('.cart--total--price--box').children('.cart--total--price--value').each(function () {
    $(this).fadeOut(fadeTime, function() {
      $(this).text(linePrice.toFixed(0));
      recalculateCart();
      $(this).fadeIn(fadeTime);
    });
  });  
}

/* Remove item from cart */
function removeItem(removeIcon)
{
  /* Remove row from DOM and recalc cart total */
  var productRow = $(removeIcon).parent().parent().parent();
  productRow.slideUp(fadeTime, function() {
    productRow.remove();
    recalculateCart();
  });
}


// * Cart funtionality
// Change product quantity
const changeProductQuantity = document.querySelector('#cart--product--list');

changeProductQuantity.addEventListener('click', e => {
  // * Add quantity
  if(e.target.classList.contains('quantity--up')){
    // console.log('quantity up');
    Array.from(e.target.parentNode.children).forEach((elem) => {
      if(elem.nodeName == 'INPUT'){
        const data = {
          product_id: elem.getAttribute('data-product-id'), 
          quantity: Number(elem.value) + 1}
        sendPostData('http://127.0.0.1:8000/change-product-quantity-cart', data, 'مشکلی پیش آمده')
        .then(data => {
          if(data.status == '200'){
            console.log(data);
            addOne(elem, 15);
            updateQuantity(elem);
          }
        })
        .catch(err => {
          console.log(err);
        })
        
      }
    })
  }
  // * Minus quantity
  if(e.target.classList.contains('quantity--down')){
    // console.log('quantity down');
    Array.from(e.target.parentNode.children).forEach((elem) => {
      if(elem.nodeName == 'INPUT'){
        const data = {
          product_id: elem.getAttribute('data-product-id'), 
          quantity: Number(elem.value) - 1}
        sendPostData('http://127.0.0.1:8000/change-product-quantity-cart', data, 'مشکلی پیش آمده')
        .then(data => {
          if(data.status == '200'){
            console.log(data);
            minuseOne(elem);
            updateQuantity(elem);
          }
        })
        .catch(err => {
          console.log(err);
        })
      }
    })
  }
})


// Integration of pure JS and Jquery!!!
// $('.cart--product-removal').click( function() {
$('.cart--remove--icon').click( function() {
  Swal.fire({
    title: 'حذف محصول',
    text: "آیا از حذف این محصول از سبد خرید خود مطمئنید؟",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#37eb34',
    cancelButtonColor: '#eb3434',
    confirmButtonText: 'بله',
    cancelButtonText: 'خیر',
  }).then((result) => {
    if (result.isConfirmed) {
      let data = {product_id: this.getAttribute('data-product-id')};
      sendPostData('http://127.0.0.1:8000/delete-product-cart', data, 'مشکلی پیش آمده')
      .then(data => {
        console.log(data)
        if(data.status == 200){
          removeItem(this);
          Swal.fire(
            'پاک شد!',
            'محصول از سبد خرید حذف شد',
            'success'
          )
        }
      })
      .catch(err => {
        console.log(err);
        Swal.fire({
          icon: 'error',
          title: 'مشکلی پیش آمده',
          text: 'محصول حذف نشد',
        })
      })
    }
    else{
      Swal.fire('محصول در سبد خرید باقی ماند')
    }
  })
  .catch(error => {
    console.log(error);
    alert('SWAL کار نمی کند');
  })
});