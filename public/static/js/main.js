/* SkillsBridge Main UI Interaction Script */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Hide Preloader on Window Load
    const preloader = document.getElementById('preloader');
    if (preloader) {
        window.addEventListener('load', () => {
            setTimeout(() => {
                preloader.classList.add('fade-out');
            }, 300);
        });
        // Fallback hide in 2 seconds
        setTimeout(() => {
            if (preloader && !preloader.classList.contains('fade-out')) {
                preloader.classList.add('fade-out');
            }
        }, 2000);
    }

    // 2. Mobile & Tablet Navigation Toggle Handler
    const mobileBtn = document.getElementById('mobileNavBtn');
    const navMenu = document.getElementById('navLinksMenu');

    if (mobileBtn && navMenu) {
        mobileBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            navMenu.classList.toggle('active');
            mobileBtn.textContent = navMenu.classList.contains('active') ? '✕' : '☰';
        });

        document.addEventListener('click', (e) => {
            if (!navMenu.contains(e.target) && !mobileBtn.contains(e.target)) {
                navMenu.classList.remove('active');
                mobileBtn.textContent = '☰';
            }
        });
    }

    // 3. Profile Avatar Dropdown Toggle Handler
    const avatarBtn = document.getElementById('avatarDropdownBtn');
    const avatarDropdown = document.getElementById('avatarDropdownMenu');

    if (avatarBtn && avatarDropdown) {
        avatarBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            avatarDropdown.classList.toggle('active');
        });

        document.addEventListener('click', (e) => {
            if (!avatarDropdown.contains(e.target) && !avatarBtn.contains(e.target)) {
                avatarDropdown.classList.remove('active');
            }
        });
    }

    // 4. Auto-dismiss Flash Alerts
    const flashMessages = document.querySelectorAll('.flash-item');
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            msg.style.transform = 'translateY(-10px)';
            msg.style.transition = 'all 0.4s ease';
            setTimeout(() => msg.remove(), 400);
        }, 5000);
    });

    // 5. Animate Radial Match Score Gauges
    const gauges = document.querySelectorAll('.radial-gauge');
    gauges.forEach(gauge => {
        const score = parseInt(gauge.dataset.score || '0');
        const circle = gauge.querySelector('.radial-fill');
        const text = gauge.querySelector('.radial-text');
        
        if (circle && text) {
            const circumference = 2 * Math.PI * 40;
            const offset = circumference - (score / 100) * circumference;
            circle.style.strokeDasharray = `${circumference}`;
            
            setTimeout(() => {
                circle.style.strokeDashoffset = `${offset}`;
                text.textContent = `${score}%`;
            }, 100);

            if (score >= 80) {
                circle.classList.add('score-high');
                text.classList.add('score-high');
            } else if (score >= 50) {
                circle.classList.add('score-med');
                text.classList.add('score-med');
            } else {
                circle.classList.add('score-low');
                text.classList.add('score-low');
            }
        }
    });

    // 6. Modal Manager
    window.openModal = function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        }
    };

    window.closeModal = function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('active');
            document.body.style.overflow = 'auto';
        }
    };

    document.querySelectorAll('.modal-overlay').forEach(overlay => {
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                overlay.classList.remove('active');
                document.body.style.overflow = 'auto';
            }
        });
    });
});
