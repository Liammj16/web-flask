const carouselSlide = document.querySelector('.carousel-slide');
        const slides = document.querySelectorAll('.slide');
        const dots = document.querySelectorAll('.dot');
        let currentIndex = 0;

        function goToSlide(index) {
            if (index < 0 || index >= slides.length) return;
            carouselSlide.style.transform = `translateX(-${index * 100}%)`;
            updateDots(index);
            currentIndex = index;
        }

        function updateDots(index) {
            dots.forEach((dot, i) => {
                dot.classList.toggle('active', i === index);
            });
        }

        function nextSlide() {
            currentIndex = (currentIndex + 1) % slides.length;
            goToSlide(currentIndex);
        }

        function prevSlide() {
            currentIndex = (currentIndex - 1 + slides.length) % slides.length;
            goToSlide(currentIndex);
        }

        // Inicializar el carrusel
        goToSlide(0);