// Простой скрипт для добавления интерактивности
document.addEventListener('DOMContentLoaded', function() {
    // Элементы мобильного меню
    const burgerBtn = document.querySelector('.burger-btn');
    const mobileMenu = document.querySelector('.mobile-menu');
    const mobileCloseBtn = document.querySelector('.mobile-close-btn');
    const menuOverlay = document.querySelector('.menu-overlay');
    const mobileNavLinks = document.querySelectorAll('.mobile-nav-link');
    const body = document.body;
    
    // Открытие мобильного меню
    function openMobileMenu() {
        mobileMenu.classList.add('active');
        menuOverlay.classList.add('active');
        body.classList.add('menu-open');
        document.body.style.overflow = 'hidden';
        if (burgerBtn) burgerBtn.setAttribute('aria-expanded', 'true');
    }
    
    // Закрытие мобильного меню
    function closeMobileMenu() {
        mobileMenu.classList.remove('active');
        menuOverlay.classList.remove('active');
        body.classList.remove('menu-open');
        document.body.style.overflow = '';
        if (burgerBtn) burgerBtn.setAttribute('aria-expanded', 'false');
    }
    
    if (burgerBtn) {
        burgerBtn.addEventListener('click', function() {
            if (mobileMenu.classList.contains('active')) {
                closeMobileMenu();
            } else {
                openMobileMenu();
            }
        });
    }
    
    if (mobileCloseBtn) mobileCloseBtn.addEventListener('click', closeMobileMenu);
    if (menuOverlay) menuOverlay.addEventListener('click', closeMobileMenu);
    
    mobileNavLinks.forEach(link => {
        link.addEventListener('click', closeMobileMenu);
    });
    
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && mobileMenu && mobileMenu.classList.contains('active')) {
            closeMobileMenu();
        }
    });
    
    // Эффект плавного скролла для ссылок навигации
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            
            e.preventDefault();
            const targetElement = document.querySelector(href);
            
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
                
                if (mobileMenu && mobileMenu.classList.contains('active')) {
                    closeMobileMenu();
                }
            }
        });
    });
    
    // Эффект уменьшения шапки при скролле
    window.addEventListener('scroll', function() {
        const header = document.querySelector('.header');
        const logoText = header ? header.querySelector('.logo-text') : null;
        if (header && logoText) {
            if (window.scrollY > 50) {
                header.style.padding = '10px 0';
                logoText.style.fontSize = '1.3rem';
            } else {
                header.style.padding = '20px 0';
                logoText.style.fontSize = '1.5rem';
            }
        }
    });
    
    // Анимация появления карточек при скролле
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.category-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(card);
    });
});
