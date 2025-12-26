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
      if (document.getElementById('feedbackModal')?.style.display === 'flex') {
        closeModal('feedbackModal');
      }
    }
  });

  // Feedback modal functionality
  const feedbackModal = document.getElementById('feedbackModal');
  const addFeedbackBtn = document.getElementById('addFeedbackBtn');
  const feedbackForm = document.getElementById('feedbackForm');

  addFeedbackBtn?.addEventListener('click', (event) => {
    event.preventDefault();
    openModal('feedbackModal');
  });

  feedbackForm?.addEventListener('submit', async (event) => {
    event.preventDefault();
    
    const name = document.getElementById('reviewName').value.trim();
    const comment = document.getElementById('reviewComment').value.trim();
    const submitBtn = feedbackForm.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    
    if (!name || !comment) {
      alert('Please fill in all fields.');
      return;
    }
    
    // Disable button and show loading state
    submitBtn.disabled = true;
    submitBtn.textContent = 'Submitting...';
    
    try {
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
      const url = feedbackForm.getAttribute('data-url');
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ name, comment }),
      });
      
      const data = await response.json();
      
      if (data.success) {
        // Add new review to the page
        const reviewsContainer = document.getElementById('reviews-container');
        const newReviewCard = document.createElement('div');
        newReviewCard.className = 'light-card review-card';
        newReviewCard.style.cssText = 'width:300px; position:relative; padding:40px 30px; border-radius:20px; text-align:left; animation:fadeIn 0.5s ease-in;';
        newReviewCard.innerHTML = `
          <div style="position:absolute; top:-15px; left:20px; background-color:var(--primary); border-radius:50%; width:50px; height:50px; display:flex; justify-content:center; align-items:center; font-size:1.2em; color:#fff; font-weight:bold;"><i class="fas fa-quote-left"></i></div>
          <p style="font-style:italic; margin-bottom:15px; margin-top:20px; color:#ffffff;">"${data.review.comment}"</p>
          <p style="font-weight:700; color:var(--primary);">— ${data.review.name}</p>
        `;
        reviewsContainer.insertBefore(newReviewCard, reviewsContainer.firstChild);
        
        // Reset form and close modal
        feedbackForm.reset();
        closeModal('feedbackModal');
        alert('Thank you for your feedback!');
      } else {
        alert(data.error || 'Failed to submit feedback. Please try again.');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred. Please try again.');
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = originalText;
    }
  });

  window.openModal = openModal;
  window.closeModal = closeModal;
});

