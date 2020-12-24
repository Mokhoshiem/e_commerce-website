let updateBtns = document.querySelectorAll('.update-cart');
    

updateBtns.forEach(e => {
    e.addEventListener('click', function(){
        'use strict';
        let productId = this.dataset.product,
            action = this.dataset.action,
            user = getCurrentUser();
        // console.log('productId: ', productId, 'Action: ', action, 'currentUser: ', user)
        if (user === 'AnonymousUser'){
            console.log('Hey, you are not logged in');
            addCookieItemToCart(productId, action);
            
        }else{
            updateCart(productId, action);
        }
    });
});

// Adding items to cart cookie
function addCookieItemToCart(productId, action){
    'use strict';
    if (action == 'add'){
        // cart is the cookie from base.js
        if (cart[productId] == undefined || cart[productId] == 'undefined'){
            cart[productId] = {'quantity':1};
        }else{
            cart[productId]['quantity'] += 1;
        }
        console.log('Item Added....')
    }

    if(action == 'remove'){
        cart[productId]['quantity'] -= 1;
        if (cart[productId]['quantity'] <= 0 ){
            delete cart[productId];
        }
        console.log('Item Removed....')
    }
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
}

//  The fetch api
function updateCart(product, action) {
    console.log('sending data ......')
    var url = '/update/' // the url for the JsonResponse view
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken
        },
        mode:'same-origin',
        body : JSON.stringify({'productId':product,'action':action})
    }).then((response) => {
        return response.json();
    }).then((data) => {
        console.log('data: ', data);
        location.reload();
    })
}

