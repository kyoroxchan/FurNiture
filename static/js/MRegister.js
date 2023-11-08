const wrapper = document.querySelector('.wrapper');
const nextLink = document.querySelector('.next');
const backLink = document.querySelector('.back');
const buttonLink = document.querySelector('.button');
nextLink.addEventListener('click', () => {
    console.log(wrapper);
    wrapper.classList.add('active');
})
backLink.addEventListener('click', () => {
    wrapper.classList.remove('active');
})
buttonLink.addEventListener('click', () => {
    wrapper.classList.remove('active');
})