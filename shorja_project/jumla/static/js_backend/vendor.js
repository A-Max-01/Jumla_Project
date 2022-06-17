function delete_image(ev) {
    console.log(ev.currentTarget.parentElement)
    let product_id = ev.currentTarget.dataset.product_id
    let  image_url = ev.currentTarget.dataset.image_url
     fetch('http://127.0.0.1:8000/vendor/delete_product', {
                   method:"PUT", body:JSON.stringify(
                       {
                           "product_id": product_id,
                           "image_url": image_url,
                           "type" : "delete_image"
                       }
                   )
               })
        .then(rep => rep.json())
            .then(data => { console.log(data)})
    ev.currentTarget.parentElement.parentNode.remove()
}

document.addEventListener('DOMContentLoaded', function(){
    console.log('run')
    let btn = document.querySelectorAll('#btn')
    let is_active_checkbox = document.querySelectorAll('#is_activ')
    let image_delete_icon = document.querySelectorAll('#delete_image')
    image_delete_icon.forEach((ele)=>{
        ele.addEventListener('click', delete_image)
    })
    is_active_checkbox.forEach((ele)=>{
        ele.addEventListener('change', update_checkbox)
    })

     btn.forEach((ele)=>{
        ele.addEventListener('click', delete_product);
    })

})

function delete_product(ev){
    let product_id = ev.currentTarget.dataset.product_id
    console.log(product_id)
    fetch('http://127.0.0.1:8000/vendor/delete_product', {
                   method:"PUT", body:JSON.stringify(
                       {
                           "product_id": product_id,
                           "type" : "delete"
                       }
                   )
               })
        .then(rep => rep.json())
            .then(data => { console.log(data)})

    ev.currentTarget.parentElement.parentElement.remove()

}
function update_checkbox(ev) {
    let product_id = ev.currentTarget.dataset.product_id
    console.log(product_id)
    fetch('http://127.0.0.1:8000/vendor/delete_product', {
                   method:"PUT", body:JSON.stringify(
                       {
                           "product_id": product_id,
                           "type" : "update_checkbox"
                       }
                   )
               })
        .then(rep => rep.json())
            .then(data => { console.log(data)})
}