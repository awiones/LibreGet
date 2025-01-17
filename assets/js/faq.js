document.addEventListener('DOMContentLoaded', () => {
    const faqItems = document.querySelectorAll('.faq-toggle');

    faqItems.forEach(item => {
        item.addEventListener('change', function() {
            const answer = this.nextElementSibling.nextElementSibling;
            answer.style.maxHeight = this.checked ? `${answer.scrollHeight}px` : '0';
        });
    });
});