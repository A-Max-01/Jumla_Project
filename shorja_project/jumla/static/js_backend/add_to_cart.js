document.addEventListener('DOMContentLoaded', function() {
check_cart_items()
     document.addEventListener('click', ev => {
           let element = ev.target;
       if(element.className==='btn btn-primary')
       {
           if(element.id !== ""){
               console.log(element.id)
               button_toggle(element)
               fetch('shopper/add-to-cart', {
                   method:"PUT", body:JSON.stringify(
                       {
                           "product_id": element.id,
                       }
                   )
               })
                   .then(rep => rep.json())
            .then(data => {console.log(data)})
               console.log(element.innerHTML)


           }else{
               console.log("don't play with me")
           }

       }else{
            console.log("please click the blue button to add to your card")
       }
     })
})
function button_toggle(element){
    if (element.innerHTML==='اضف الى السلة'){
        element.innerHTML="حذف"
    }else{
        element.innerHTML='اضف الى السلة'
    }
}

function  check_cart_items(){
    btn = document.querySelectorAll('.btn')
    fetch('shopper/check_item_in_bill_order')
    .then(rep => rep.json())
    .then(data => {
        btn.forEach(function (ele){
            if(data.items_in_cart.includes(parseInt(ele.id))){
                ele.innerHTML = "حذف"
            }else{
                ele.innerHTML = "اضف الى السلة"
            }
    })
    })
}
