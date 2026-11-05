// Mobile menu toggle
const toggle = document.querySelector('.menu-toggle');
const links = document.querySelector('.nav-links');
if (toggle && links) {
  toggle.addEventListener('click', () => links.classList.toggle('open'));
  links.querySelectorAll('a').forEach(a => a.addEventListener('click', () => links.classList.remove('open')));
}

// Smooth scroll with nav offset
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      window.scrollTo({ top: target.offsetTop - 64, behavior: 'smooth' });
    }
  });
});

// Staggered Fade-in on scroll
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry, index) => {
    if (entry.isIntersecting) {
      // Stagger the delay for cards
      entry.target.style.transitionDelay = `${index * 0.1}s`;
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
      observer.unobserve(entry.target); // Stop observing once it's visible
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.card, .stat, .tl-item, .blog-item, .detail-block').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(30px)';
  el.style.transition = 'opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1), transform 0.6s cubic-bezier(0.16, 1, 0.3, 1)';
  observer.observe(el);
});

// Typing Animation for Hero
const text = "Automation Engineer";
const speed = 100; 
let i = 0;

function typeWriter() {
  const target = document.querySelector(".grad");
  if (target) {
    target.innerHTML = ""; 
    function type() {
      if (i < text.length) {
        target.innerHTML += text.charAt(i);
        i++;
        setTimeout(type, speed);
      }
    }
    // Start typing after a 500ms delay
    setTimeout(type, 500); 
  }
}
typeWriter();

// Highlight active nav link
const path = location.pathname.split('/').pop() || 'index.html';
document.querySelectorAll('.nav-links a').forEach(a => {
  if (a.getAttribute('href') === path) a.classList.add('active');
});