document.addEventListener('DOMContentLoaded', function() {

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
