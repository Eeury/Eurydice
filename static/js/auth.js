function checkPasswordStrength() {
    const password = document.getElementById('password');
    if (!password) return;
    
    const passwordValue = password.value;
    const cap = document.getElementById('req-capital');
    const num = document.getElementById('req-number');
    const spec = document.getElementById('req-special');
    const button = document.getElementById('signup-button');
    
    if (!cap || !num || !spec || !button) return;
    
    // Check for 1 Capital Letter (A-Z)
    const hasCapital = /[A-Z]/.test(passwordValue);
    cap.className = hasCapital ? 'valid' : 'invalid';
    
    // Check for 1 Number (0-9)
    const hasNumber = /[0-9]/.test(passwordValue);
    num.className = hasNumber ? 'valid' : 'invalid';
    
    // Check for 1 Special Character (using a common set)
    const hasSpecial = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(passwordValue);
    spec.className = hasSpecial ? 'valid' : 'invalid';

    const isStrong = hasCapital && hasNumber && hasSpecial;
    
    // Enable/Disable button based on requirements
    if (isStrong) {
        button.disabled = false;
        button.style.opacity = '1.0';
        button.style.cursor = 'pointer';
    } else {
        button.disabled = true;
        button.style.opacity = '0.6';
        button.style.cursor = 'not-allowed';
    }
}

// Validate form on submit
document.addEventListener('DOMContentLoaded', function() {
    const signupForm = document.getElementById('signup-form');
    if (signupForm) {
        signupForm.addEventListener('submit', function(e) {
            const password = document.getElementById('password');
            const confirmPassword = document.getElementById('confirm-password');
            
            if (!password || !confirmPassword) return;
            
            if (password.value !== confirmPassword.value) {
                e.preventDefault();
                alert("Error: Passwords do not match.");
                return false;
            }
            
            // This re-checks strength, though it should be strong if the button is enabled
            if (!(/[A-Z]/.test(password.value) && /[0-9]/.test(password.value) && /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password.value))) {
                e.preventDefault();
                alert("Error: Password does not meet all requirements.");
                return false;
            }
        });
        checkPasswordStrength();
    }
});

