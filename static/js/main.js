function changeSlider() {
  position -= slideSize;
    
  if (position < -(slideSize * 2))
      position = 0;
  slides.style.left = position + 'px';  
}
let position = 0;
let slideSize = 1000;
let motion = setInterval(changeSlider, 4000);