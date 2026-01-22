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
        body.classList.add('menu-open'); // Добавляем класс к body для скрытия логотипа и бургер-кнопки
        document.body.style.overflow = 'hidden'; // Отключаем скролл страницы
        burgerBtn.setAttribute('aria-expanded', 'true');
    }
    
    // Закрытие мобильного меню
    function closeMobileMenu() {
        mobileMenu.classList.remove('active');
        menuOverlay.classList.remove('active');
        body.classList.remove('menu-open'); // Убираем класс с body для показа логотипа и бургер-кнопки
        document.body.style.overflow = ''; // Восстанавливаем скролл страницы
        burgerBtn.setAttribute('aria-expanded', 'false');
    }
    
    // Обработчики событий для открытия/закрытия меню
    burgerBtn.addEventListener('click', function() {
        if (mobileMenu.classList.contains('active')) {
            closeMobileMenu();
        } else {
            openMobileMenu();
        }
    });
    
    mobileCloseBtn.addEventListener('click', closeMobileMenu);
    menuOverlay.addEventListener('click', closeMobileMenu);
    
    // Закрытие меню при клике на ссылку
    mobileNavLinks.forEach(link => {
        link.addEventListener('click', closeMobileMenu);
    });
    
    // Закрытие меню при нажатии клавиши Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && mobileMenu.classList.contains('active')) {
            closeMobileMenu();
        }
    });
    
    // Эффект плавного скролла для ссылок навигации
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // Пропускаем ссылки, которые не ведут на якоря на текущей странице
            if (href === '#') return;
            
            e.preventDefault();
            const targetElement = document.querySelector(href);
            
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
                
                // Закрываем мобильное меню если оно открыто
                if (mobileMenu.classList.contains('active')) {
                    closeMobileMenu();
                }
            }
        });
    });
    
    // Эффект уменьшения шапки при скролле
    window.addEventListener('scroll', function() {
        const header = document.querySelector('.header');
        if (window.scrollY > 50) {
            header.style.padding = '10px 0';
            header.querySelector('.logo-text').style.fontSize = '1.3rem';
        } else {
            header.style.padding = '20px 0';
            header.querySelector('.logo-text').style.fontSize = '1.5rem';
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
    
    // Наблюдаем за карточками категорий
    document.querySelectorAll('.category-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(card);
    });
});