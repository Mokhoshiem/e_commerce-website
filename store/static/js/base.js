function getToken(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
  }
  return cookieValue;
}
const csrftoken = getToken('csrftoken');

function getCookie(name){
    // getting all cookie
    const cookieArray = document.cookie.split(';');
    // looping through cookiearray
    // console.log(cookieArray);
    cookieArray.forEach(c => {
        let cookiePair = c.split('=');
        // console.log(cookiePair)
        if (name == cookiePair[0].trim) {
            return decodeURIComponent(cookiePair[1].trim);
        }
        console.log(cookiePair[0],": " ,cookiePair[1])
    })
    return null;
}

var cart = JSON.parse(getCookie('cart'));
// getCookie('cart');
if (cart == undefined || cart == 'undefined' || cart == null) {
    cart = {}
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
}
