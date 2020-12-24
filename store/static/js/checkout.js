function oncall (){
    
    let user = getCurrentUser(),
        form = document.querySelector('.checkout-form'),
        altConfirm = document.querySelector('.alt-confirm');
        

    if (user !== 'AnonymousUser'){
        form.style.display = 'none';
        altConfirm.classList.remove('hidden');
        altConfirm.addEventListener('click', function(){
            getFormData();
            fetching()
        })
        }else{
            form.addEventListener('submit', function(e){
                e.preventDefault();
                getFormData();
                fetching();
            })
            
        }
        
    function getFormData(){
        data = data ={ 'userData' : {
            'username':form.username.value,
            'tel1':form.tel1.value
        },
        'shippingInfo' : {
            'address':form.address.value,
            'city':form.city.value,
            'state':form.state.value
        }};
        return data
    }

    function fetching(){
        url = '/confirm/'
        fetch(url, {
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken':csrftoken
            },
            mode:'same-origin',
            body:JSON.stringify({'userData':data.userData, 'shippingInfo':data.shippingInfo})
            
            }).then((response) => response.json()).then((data) => {
                console.log(data)
                alert('تم تأكيد الطلب جاري مراجعة الطلب و الشحن')
                window.location.href = "done"
        })
    }
    
}


oncall()