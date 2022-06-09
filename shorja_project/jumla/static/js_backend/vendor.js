

document.addEventListener('DOMContentLoaded', function(){
    console.log('run')
    let btn = document.querySelectorAll('#btn')
    let is_active_checkbox = document.querySelectorAll('#is_activ')

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