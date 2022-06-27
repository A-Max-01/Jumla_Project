document.addEventListener('DOMContentLoaded', function(){
    console.log('run')
    let btn = document.querySelectorAll('#btn')
    fetch('http://127.0.0.1:8000/shopper/check_item_in_bill_order')
    .then(rep => rep.json())
    .then(data => {
        btn.forEach((ele)=>{
            // console.log(ele.dataset.product_id)
            if(data.items_in_cart.includes(parseInt(ele.dataset.product_id))){
                // console.log('true')
                ele.innerHTML='حذف'

            }else{
                // console.log('false')
                ele.innerHTML='اضف الى السلة'
                // ele.className = 'btn btn-primary'
            }
        })
    })

    btn.forEach((ele)=>{
        ele.addEventListener('click', add_or_remove_item_from_cart);
    })

    let input_qty = document.querySelectorAll('#qty')
    // console.log(input_qty);
    input_qty.forEach((ele)=>{
        ele.addEventListener('change', func)
    })


})
function func(ev){
    // console.log("change function")
    let product_id = ev.currentTarget.dataset.product_id
    let qty = ev.currentTarget.value
    let cart_total = document.getElementById('cart_total')

    if(qty >=1 && qty <=50){
        if(product_id){
            let total = document.getElementById(ev.currentTarget.dataset.bill_id)
             console.log('between range')
        fetch('http://127.0.0.1:8000/shopper/update_quentity',{
        method:'PUT',
        body:JSON.stringify({
            "product_id": product_id,
            'qty':qty
        })
    })
         .then(rep => rep.json())
            .then(data => {
                if(total){
            console.log('have total')
                      total.textContent = data.bill_total
                        cart_total.textContent = data.cart_total
        }else{
            console.log('not have total')
        }
            })
    }
        }

    else {
        console.log('false')
    }

}
function add_or_remove_item_from_cart(ev){
    let product_id = ev.currentTarget.dataset.product_id
    let cart_total = document.getElementById('cart_total')
    if(product_id){
        button_toggle(ev.currentTarget)
    let bill_total = document.getElementById(ev.currentTarget.dataset.bill_id)

        fetch('http://127.0.0.1:8000/shopper/add-to-cart', {
                   method:"PUT", body:JSON.stringify(
                       {
                           "product_id": product_id,
                       }
                   )
               })
                   .then(rep => rep.json())
            .then(data => {
                  if(bill_total){
            console.log('have total')
                      bill_total.textContent = data.bill_total
                      cart_total.textContent = data.cart_total
        }else{
            console.log('not have total')
        }

            })
    }else{
        console.log('not ok')
    }
}
function button_toggle(element){
    // console.log(element.innerHTML)
    if (element.innerHTML==='اضف الى السلة'){
        element.innerHTML="حذف"
        // element.className = 'btn btn-danger'
    }else{
        element.innerHTML='اضف الى السلة'
        // element.className = 'btn btn-primary'
    }
}
