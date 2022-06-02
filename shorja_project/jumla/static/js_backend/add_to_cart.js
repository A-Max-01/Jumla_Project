document.addEventListener('DOMContentLoaded', function() {
check_cart_items()
     document.addEventListener('click', ev => {
           let element = ev.target;
           console.log(element.value)
          let total = element.parentElement.parentNode.parentNode.parentElement.childNodes[1].childNodes[1].childNodes[3].childNodes[3]
         // console.log(total)
         if(element.id==='qty'){
             console.log(element.value)
         }else {
             console.log('is not a qty')
         }
       if(element.className==='btn btn-primary')
       {
           if(element.id !== ""){
               // console.log(element.id)
               button_toggle(element)
               // fetch('shopper/add-to-cart', {
               fetch('http://127.0.0.1:8000/shopper/add-to-cart', {
                   method:"PUT", body:JSON.stringify(
                       {
                           "product_id": element.id,
                       }
                   )
               })
                   .then(rep => rep.json())
            .then(data => {
                console.log(data.total)
                total.textContent = data.total
            })


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
// http://127.0.0.1:8000/shopper/add-to-cart

function  check_cart_items(){
    btn = document.querySelectorAll('.btn')
    fetch('http://127.0.0.1:8000/shopper/check_item_in_bill_order')
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
