// Adicionar/remover classe para mudar opacidade do header
window.addEventListener('scroll', function () {
    const header = document.getElementById('main-header');
    if (window.scrollY > 50) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  });

  // Movimento do carrossel

  const testimonials = document.querySelectorAll(".testimonial");
  let currentIndex = 0;
  let intervalId = null;
  
  // Função que exibe o depoimento no índice indicado
  function showTestimonial(index) {
    testimonials.forEach((testimonial, i) => {
      testimonial.classList.remove("active");
      if (i === index) {
        testimonial.classList.add("active");
      }
    });
  }
  
  // Botões de navegação
  document.getElementById("prev-btn").addEventListener("click", () => {
    currentIndex = (currentIndex - 1 + testimonials.length) % testimonials.length;
    showTestimonial(currentIndex);
  });
  
  document.getElementById("next-btn").addEventListener("click", () => {
    currentIndex = (currentIndex + 1) % testimonials.length;
    showTestimonial(currentIndex);
  });
  
  // Autoplay a cada 3 segundos
  function startAutoplay() {
    intervalId = setInterval(() => {
      currentIndex = (currentIndex + 1) % testimonials.length;
      showTestimonial(currentIndex);
    }, 3000); 
  }
  
  // Pausa o autoplay
  function stopAutoplay() {
    clearInterval(intervalId);
  }
  
  // Iniciar autoplay ao carregar a página
  document.addEventListener("DOMContentLoaded", () => {
    showTestimonial(currentIndex);
    startAutoplay();
  
    // Detecta a área de hover
    const carousel = document.querySelector(".testimonial-carousel");
  
    carousel.addEventListener("mouseenter", () => {
      stopAutoplay(); // Pausa ao passar o mouse
    });
  
    carousel.addEventListener("mouseleave", () => {
      startAutoplay(); // Retoma ao tirar o mouse
    });
  });
  