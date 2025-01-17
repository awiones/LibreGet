// Platform detection and download button customization
document.addEventListener('DOMContentLoaded', () => {
    const detectPlatform = () => {
        const userAgent = window.navigator.userAgent.toLowerCase();
        if (userAgent.includes('windows')) return { name: 'Windows', icon: 'fa-windows' };
        if (userAgent.includes('mac')) return { name: 'macOS', icon: 'fa-apple' };
        return { name: 'Linux', icon: 'fa-linux' };
    };

    const platform = detectPlatform();
    const platformText = document.getElementById('platform-text');
    if (platformText) {
        platformText.textContent = `Download for ${platform.name}`;
    }

    // Update all download buttons with platform-specific info
    document.querySelectorAll('.download-btn').forEach(btn => {
        if (!btn.classList.contains('primary')) {
            const platformIcon = document.createElement('i');
            platformIcon.className = `fab ${platform.icon} me-2`;
            btn.prepend(platformIcon);
        }
    });

    // Enhanced download handling for platform-specific buttons
    document.querySelectorAll('.platform-download-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Get download details from data attributes
            const platform = btn.getAttribute('data-platform');
            const version = btn.getAttribute('data-version');
            const downloadPage = btn.getAttribute('data-url');
            
            // Create download tracking object (optional, for analytics)
            const downloadInfo = {
                platform: platform,
                version: version,
                timestamp: new Date().toISOString()
            };
            
            // Show download starting toast
            const toast = document.createElement('div');
            toast.className = 'toast';
            toast.textContent = `Preparing download for ${platform.charAt(0).toUpperCase() + platform.slice(1)} (v${version})`;
            document.body.appendChild(toast);
            
            // Redirect to download page
            window.location.href = downloadPage;
            
            // Toast animation
            setTimeout(() => {
                toast.classList.add('show');
                setTimeout(() => {
                    toast.classList.remove('show');
                    setTimeout(() => {
                        toast.remove();
                    }, 300);
                }, 3000);
            }, 100);
        });
    });
});

// Navbar scroll effect
const navbar = document.querySelector('.navbar');
let lastScroll = 0;

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > lastScroll && currentScroll > 100) {
        navbar.style.transform = 'translateY(-100%)';
    } else {
        navbar.style.transform = 'translateY(0)';
    }
    
    if (currentScroll > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
    
    lastScroll = currentScroll;
});

// Navbar dropdown functionality
const navDropdowns = document.querySelectorAll('.dropdown');

navDropdowns.forEach(dropdown => {
    const dropbtn = dropdown.querySelector('.dropbtn');
    const dropdownContent = dropdown.querySelector('.dropdown-content');

    dropbtn.addEventListener('click', (e) => {
        e.preventDefault();
        dropdown.classList.toggle('active');
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!dropdown.contains(e.target)) {
            dropdown.classList.remove('active');
        }
    });
});

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const headerOffset = 80;
            const elementPosition = target.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });

            // Close mobile menu if open
            if (mobileMenu && mobileMenu.classList.contains('active')) {
                mobileMenuBtn.click();
            }
        }
    });
});

// Animated counter for statistics
const animateValue = (element, start, end, duration) => {
    if (!element) return;
    
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const current = Math.floor(progress * (end - start) + start);
        element.textContent = current.toLocaleString();
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
};

// Intersection Observer for scroll animations
const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            
            // Handle counter animations
            if (entry.target.classList.contains('download-count')) {
                const target = parseInt(entry.target.dataset.target);
                animateValue(entry.target, 0, target, 2000);
            }
        }
    });
}, observerOptions);

// Observe elements with animation classes
document.querySelectorAll('.animate-on-scroll, .download-count').forEach(el => {
    observer.observe(el);
});

// Newsletter form submission
const newsletterForm = document.querySelector('.newsletter-form');
if (newsletterForm) {
    newsletterForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const email = newsletterForm.querySelector('input[type="email"]').value;
        
        // Simulate form submission
        const button = newsletterForm.querySelector('button');
        const originalText = button.textContent;
        button.textContent = 'Submitting...';
        button.disabled = true;
        
        // Simulate API call
        setTimeout(() => {
            button.textContent = 'Subscribed!';
            newsletterForm.reset();
            
            setTimeout(() => {
                button.textContent = originalText;
                button.disabled = false;
            }, 2000);
        }, 1500);
    });
}

// Feature card animations
document.querySelectorAll('.feature-card').forEach(card => {
    card.addEventListener('mouseenter', () => {
        const icon = card.querySelector('.feature-icon i');
        if (icon) {
            icon.style.transform = 'scale(1.2)';
            setTimeout(() => {
                icon.style.transform = 'scale(1)';
            }, 200);
        }
    });
});

// Performance animation triggers
const performanceSection = document.querySelector('.performance');
if (performanceSection) {
    const numbers = performanceSection.querySelectorAll('.performance-number');
    let animated = false;
    
    const performanceObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !animated) {
                animated = true;
                numbers.forEach(number => {
                    const target = parseFloat(number.dataset.target);
                    animateValue(number, 0, target, 2000);
                });
            }
        });
    }, {
        threshold: 0.1 // Trigger when 10% of the section is visible
    });
    
    performanceObserver.observe(performanceSection);
}

// Additional Performance Animation Function
function animatePerformanceNumbers() {
    const performanceNumbers = document.querySelectorAll('.performance-number');
    
    performanceNumbers.forEach(number => {
        const target = parseFloat(number.dataset.target);
        const duration = 2000; // 2 seconds animation
        
        let start = 0;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            number.textContent = (progress * target).toFixed(1);
            
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        
        const startTime = performance.now();
        window.requestAnimationFrame(step);
    });
}

// Floating download button visibility
const floatingBtn = document.querySelector('.floating-download');
if (floatingBtn) {
    const downloadSection = document.getElementById('download');
    
    window.addEventListener('scroll', () => {
        if (downloadSection) {
            const rect = downloadSection.getBoundingClientRect();
            if (rect.top > window.innerHeight || rect.bottom < 0) {
                floatingBtn.style.opacity = '1';
                floatingBtn.style.transform = 'translateY(0)';
            } else {
                floatingBtn.style.opacity = '0';
                floatingBtn.style.transform = 'translateY(100%)';
            }
        }
    });
}