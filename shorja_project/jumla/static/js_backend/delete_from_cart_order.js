document.addEventListener('DOMContentLoaded', function() {

     document.addEventListener('click', ev => {
         let element = ev.target;
        if(element.className==='btn btn-danger')
       {
           if(element.id !== ""){
               console.log(element.id)
               fetch('shopper/add-to-cart')
                   .then(rep => rep.json())
                   .then(data => {console.log(data)})
               // button_toggle(element)
            //    fetch('/add-to-cart', {
            //        method:"PUT", body:JSON.stringify(
            //            {
            //                "product_id": element.id,
            //            }
            //        )
            //    })
            //        .then(rep => rep.json())
            // .then(data => {console.log(data)})
            //    console.log(element.innerHTML)


           }else{
               console.log("don't play with me")
           }

       }else{
            console.log("please click the blue button to add to your card")
       }
     })


})



