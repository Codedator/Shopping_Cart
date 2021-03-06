var updateButtons = document.getElementsByClassName('update-cart')

for (var i=0;i < updateButtons.length; i++)
{
    updateButtons[i].addEventListener('click', function(){
        var itemId = this.dataset.item
        var action = this.dataset.action
        console.log('itemId:', itemId, 'action:', action)

        console.log('User:', user)
        if(user == 'AnonymousUser'){
            addCookieItem(itemId, action)
        }else{
            updateUserOrder(itemId, action)
        }
    })
}

function addCookieItem(itemId, action){
    console.log("Not logged in")

    if(action == 'add'){
        if (cart[itemId] == undefined){
            cart[itemId] = {'quantity': 1}
        }
        else{
            cart[itemId]['quantity'] += 1
        }
    }

    if(action == 'remove'){
        cart[itemId]['quantity'] -= 1
        if (cart[itemId]['quantity'] <= 0){
            console.log('Remove Item')
            delete cart[itemId]
        }
    }

    console.log('Cart:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"

    location.reload()

}

function updateUserOrder(itemId, action){
    console.log('User is logged in. Sending data now...')

    var url = 'update_item/'
    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'itemId': itemId, 'action': action})
    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {
        console.log('data:', data)
        location.reload()
    })
}