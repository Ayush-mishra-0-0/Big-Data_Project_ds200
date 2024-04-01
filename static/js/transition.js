document.addEventListener('DOMContentLoaded', function() {
    const leftColumn = document.querySelector('.left-column');
    const rightColumn = document.querySelector('.right-column');
    const xgboostPoints = document.querySelector('.xgboost-points');
    const images = document.querySelectorAll('.image');

    // Trigger the CSS animation
    leftColumn.style.animation = 'slideUp 0.5s ease forwards';
    rightColumn.style.animation = 'slideUp 0.5s ease forwards';
    xgboostPoints.style.animation = 'slideUp 0.5s ease forwards';
    images.forEach(image => image.style.animation = 'slideUp 0.5s ease forwards');
});
