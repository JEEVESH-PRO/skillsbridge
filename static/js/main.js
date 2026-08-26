/* SkillsBridge Main UI Interaction Script */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Auto-dismiss Flash Alerts
    const flashMessages = document.querySelectorAll('.flash-item');
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            msg.style.transform = 'translateY(-10px)';
            msg.style.transition = 'all 0.4s ease';
            setTimeout(() => msg.remove(), 400);
        }, 5000);
    });

    // 2. Animate Radial Match Score Gauges
    const gauges = document.querySelectorAll('.radial-gauge');
    gauges.forEach(gauge => {
        const score = parseInt(gauge.dataset.score || '0');
        const circle = gauge.querySelector('.radial-fill');
        const text = gauge.querySelector('.radial-text');
        
        if (circle && text) {
            const circumference = 2 * Math.PI * 40; // radius = 40
            const offset = circumference - (score / 100) * circumference;
            circle.style.strokeDasharray = `${circumference}`;
            
            setTimeout(() => {
                circle.style.strokeDashoffset = `${offset}`;
                text.textContent = `${score}%`;
            }, 100);

            // Apply color classes
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

    // 3. Modal Manager
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

    // Close modal on click outside
    document.querySelectorAll('.modal-overlay').forEach(overlay => {
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                overlay.classList.remove('active');
                document.body.style.overflow = 'auto';
            }
        });
    });
});
