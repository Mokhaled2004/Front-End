// Arrays for dynamic content
const titles = [
    "Amazing Deals",
    "Super Savings",
    "Exclusive Offers",
];

const descriptions = [
    "Discover incredible discounts on your favorite products. Don't miss out on these limited-time offers!",
    "Save big on top brands and popular items. Limited time only!",
    "Unlock exclusive deals and promotions available just for you!",
];

const links = [
    "https://example.com/deals1",
    "https://example.com/deals2",
    "https://example.com/deals3",
];

const images = [
    "/static/images/deal6.png",
    "/static/images/deal8.png",
    "/static/images/deal10.png",
];

// Function to update content
function updateContent(index) {
    const titleElement = document.getElementById('dynamic-title');
    const descriptionElement = document.getElementById('dynamic-description');
    const linkElement = document.getElementById('dynamic-link');
    const imageElement = document.getElementById('dynamic-image');

    // Update the content based on the index
    titleElement.textContent = titles[index];
    descriptionElement.textContent = descriptions[index];
    linkElement.href = links[index];
    imageElement.src = images[index];
}

// Automatically cycle through content
let currentIndex = 0;
function cycleContent() {
    updateContent(currentIndex);
    currentIndex = (currentIndex + 1) % titles.length; // Loop back to the start
}

// Start the content cycling with an interval
setInterval(cycleContent, 5000); // Change every 5 seconds

// I

document.addEventListener('DOMContentLoaded', () => {
    const leftArrow = document.querySelector('.left-arrow');
    const rightArrow = document.querySelector('.right-arrow');
    const carouselContent = document.querySelector('.carousel-content');
    const slides = document.querySelectorAll('.slide');
    const slideWidth = slides[0].offsetWidth; // Get the width of a single slide

    let currentIndex = 0;

    function updateSlides() {
        const offset = -currentIndex * slideWidth; // Move to the current slide
        carouselContent.style.transform = `translateX(${offset}px)`;
    }

    leftArrow.addEventListener('click', () => {
        if (currentIndex > 0) {
            currentIndex--;
            updateSlides();
        }
    });

    rightArrow.addEventListener('click', () => {
        if (currentIndex < slides.length - 1) {
            currentIndex++;
            updateSlides();
        }
    });

    // Initialize the carousel position
    updateSlides();
});


document.addEventListener('DOMContentLoaded', () => {
    const leftArrow2 = document.querySelector('.left-arrow3');
    const rightArrow2 = document.querySelector('.right-arrow3');
    const carouselContent2 = document.querySelector('.carousel-content3');
    const slides2 = document.querySelectorAll('.slide3');
    const slideWidth2 = slides2[0].offsetWidth; // Get the width of a single slide

    let currentIndex2 = 0;

    function updateSlides2() {
        const offset2 = -currentIndex2 * slideWidth2; // Move to the current slide
        carouselContent2.style.transform = `translateX(${offset2}px)`;
    }

    leftArrow2.addEventListener('click', () => {
        if (currentIndex2 > 0) {
            currentIndex2--;
            updateSlides2();
        }
    });

    rightArrow2.addEventListener('click', () => {
        if (currentIndex2 < slides2.length - 1) {
            currentIndex2++;
            updateSlides2();
        }
    });

    // Initialize the carousel position
    updateSlides2();
});


document.addEventListener('DOMContentLoaded', () => {
    const leftArrow2 = document.querySelector('.left-arrow4');
    const rightArrow2 = document.querySelector('.right-arrow4');
    const carouselContent2 = document.querySelector('.carousel-content4');
    const slides2 = document.querySelectorAll('.slide4');
    const slideWidth2 = slides2[0].offsetWidth; // Get the width of a single slide

    let currentIndex2 = 0;

    function updateSlides2() {
        const offset2 = -currentIndex2 * slideWidth2; // Move to the current slide
        carouselContent2.style.transform = `translateX(${offset2}px)`;
    }

    leftArrow2.addEventListener('click', () => {
        if (currentIndex2 > 0) {
            currentIndex2--;
            updateSlides2();
        }
    });

    rightArrow2.addEventListener('click', () => {
        if (currentIndex2 < slides2.length - 1) {
            currentIndex2++;
            updateSlides2();
        }
    });

    // Initialize the carousel position
    updateSlides2();
});

document.addEventListener('DOMContentLoaded', () => {
    const leftArrow2 = document.querySelector('.left-arrow5');
    const rightArrow2 = document.querySelector('.right-arrow5');
    const carouselContent2 = document.querySelector('.carousel-content5');
    const slides2 = document.querySelectorAll('.slide5');
    const slideWidth2 = slides2[0].offsetWidth; // Get the width of a single slide

    let currentIndex2 = 0;

    function updateSlides2() {
        const offset2 = -currentIndex2 * slideWidth2; // Move to the current slide
        carouselContent2.style.transform = `translateX(${offset2}px)`;
    }

    leftArrow2.addEventListener('click', () => {
        if (currentIndex2 > 0) {
            currentIndex2--;
            updateSlides2();
        }
    });

    rightArrow2.addEventListener('click', () => {
        if (currentIndex2 < slides2.length - 1) {
            currentIndex2++;
            updateSlides2();
        }
    });

    // Initialize the carousel position
    updateSlides2();
});



