document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('[data-slideshow]').forEach((container) => {
    const images = container.querySelectorAll('img');
    if (images.length <= 1) return;
    let index = 0;
    const dots = container.querySelector('[data-dots]');
    images.forEach((img, i) => {
      img.style.display = i === 0 ? 'block' : 'none';
      const dot = document.createElement('button');
      dot.className = 'dot';
      dot.textContent = '•';
      dot.addEventListener('click', () => show(i));
      dots && dots.appendChild(dot);
    });
    function show(i){
      images[index].style.display = 'none';
      index = i;
      images[index].style.display = 'block';
    }
    setInterval(()=> show((index + 1) % images.length), 4000);
  });

  const loginModal = document.getElementById('loginModal');
  const signupModal = document.getElementById('signupModal');
  const loginBtn = document.getElementById('loginBtn');
  const signupBtn = document.getElementById('signupBtn');

  const openModal = (id) => {
    const modal = document.getElementById(id);
    if (modal) {
      modal.style.display = 'flex';
      const firstInput = modal.querySelector('input[type="text"], input[type="email"], input[type="password"]');
      if (firstInput) {
        firstInput.focus();
      }
    }
  };

  const closeModal = (id) => {
    const modal = document.getElementById(id);
    if (modal) {
      modal.style.display = 'none';
    }
  };

  loginBtn?.addEventListener('click', (event) => {
    event.preventDefault();
    openModal('loginModal');
  });

  signupBtn?.addEventListener('click', (event) => {
    event.preventDefault();
    openModal('signupModal');
  });

  window.addEventListener('click', (event) => {
    if (event.target.classList && event.target.classList.contains('modal-overlay')) {
      event.target.style.display = 'none';
    }
  });

  window.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      if (loginModal?.style.display === 'flex') {
        closeModal('loginModal');
      }
      if (signupModal?.style.display === 'flex') {
        closeModal('signupModal');
      }
    }
  });

  window.openModal = openModal;
  window.closeModal = closeModal;
});

