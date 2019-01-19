'use strict'

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var CartModule = (function(){

    function ajax(options) {
        return new Promise(function (resolve, reject) {
          $.ajax(options).done(resolve).fail(reject);
        });
    }

    /**
     * Update product count
     * @param {Number} productCount new product count
     */
    function updateProductCount(data){
        var element = $("#productCount")[0]
        if (element) {
            element.innerHTML = data['productCount']
        }
        changeCartCount(data['cartCount'])     
    }

    /**
     * Remove div of product element from html markup
     * @param {Object} element button of element with need to remove
     * @package {Number} cartCount new count of product in cart
     */
    function removeProductFromHtmlCart(element, cartCount){
        if (!element) {
            throw "Element not specified"
        }
        var productDiv = element.closest("#product")
        $(productDiv).hide(800,function(){
            productDiv.parentNode.removeChild(productDiv);
            changeCartCount(cartCount)
        })
    }

    /**
     * Set cart count in html
     * @param {Number} cartCount new cart count
     */
    function changeCartCount(cartCount) {
        var cartCountSpan = $("#cartCount")[0]
        if (!cartCountSpan) {
            throw "Element not specified"
        }
        cartCountSpan.innerHTML = cartCount
    }
    
    return {
        /**
         * Remove product from cart
         * @param {number} productId id of product
         */
        removeProductFromCart : function(productId, element) {          
            ajax({
                url: '/ajax/cart/remove/product',
                type: 'POST',
                dataType: 'text',
                async : true,
                data : {'id' : productId, csrfmiddlewaretoken : getCookie('csrftoken')},
            }).then(function (data){
                removeProductFromHtmlCart(element, JSON.parse(data)['cartCount'])                
            }).catch(function(error){
                console.log(error)
            })
        },

        /**
         * Increase or decrease product count in cart
         * @param {Number} productId id of product
         * @param {String} operation type of operation add or remove
         */
        changeProductCountInCart : function(productId, operation) {
            ajax({
                url: '/ajax/cart/chage/product/count',
                type: 'POST',
                dataType: 'text',
                async : true,
                data : {'id' : productId, 'operation' : operation, csrfmiddlewaretoken : getCookie('csrftoken')},
            }).then(function (data){
                updateProductCount(JSON.parse(data))
            }).catch(function(error){
                console.log(error)
            })
        },
    }
})();