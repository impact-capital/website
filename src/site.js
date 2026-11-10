(function(){
  var nav=document.querySelector('.nav');
  function onScroll(){if(nav)nav.classList.toggle('solid',window.scrollY>40||!document.querySelector('.hero,.co-hero'));}
  onScroll();window.addEventListener('scroll',onScroll,{passive:true});
  var slides=[].slice.call(document.querySelectorAll('.hero .slide')),dots=[].slice.call(document.querySelectorAll('.dots button')),i=0,t;
  function go(n){if(!slides.length)return;slides[i].classList.remove('is-on');dots[i]&&dots[i].classList.remove('on');i=(n+slides.length)%slides.length;slides[i].classList.add('is-on');dots[i]&&dots[i].classList.add('on');}
  function play(){clearInterval(t);if(!matchMedia('(prefers-reduced-motion: reduce)').matches)t=setInterval(function(){go(i+1)},6500);}
  dots.forEach(function(d){d.addEventListener('click',function(){go(+d.dataset.go);play();});});
  play();
  document.addEventListener('click',function(ev){var l=document.querySelector('.lang[open]');if(l&&!l.contains(ev.target))l.removeAttribute('open');});
  document.querySelectorAll('.lang a').forEach(function(a){a.addEventListener('click',function(){window.dataLayer&&dataLayer.push({event:'language_switch',language:a.getAttribute('hreflang')});});});
})();
