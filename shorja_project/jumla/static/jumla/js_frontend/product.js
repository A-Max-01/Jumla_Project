document.addEventListener('DOMContentLoaded', () => {

/*product slider*/



const buttons = document.querySelectorAll('.button');
const hiddens = document.querySelectorAll('.hidden');

buttons.forEach((btn) => {
  btn.addEventListener('click', btnClicked)
  
  function btnClicked(e) {    
    hiddens.forEach((hidden) => {
      if(e.target.dataset.btn == hidden.dataset.content) {
        hidden.classList.toggle('height')
      } else {
        hidden.classList.remove('height')
      }
    })
}
})







let tabs = Array.from(document.querySelectorAll('.subnavBtn'));
let contents = Array.from(document.querySelectorAll('.subnavDiv'));


const handleClick = (e,btn) => {
  e.preventDefault();
  tabs.forEach(node => {
    node.classList.remove('active-btn');
  });
  e.currentTarget.classList.add('active-btn');
  contents.forEach(x => x.classList.remove('active'))
  btn.classList.add('active');

}

tabs.forEach((node,i) => {
  node.addEventListener('click',(e) => handleClick(e,contents[i]))
});

});