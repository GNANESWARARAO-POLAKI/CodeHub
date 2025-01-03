// Theme management
const THEMES = {
    light: 'light',
    dark: 'dark'
};

function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    updateToggleButtonText(theme);
    
}

function updateToggleButtonText(theme) {
    const toggleButton = document.getElementById('toggle_button');
    toggleButton.textContent = theme === THEMES.dark ? '🔆' : '🌜';
}

// Initialize theme
const savedTheme = localStorage.getItem('theme') || THEMES.dark; // Default to dark theme
setTheme(savedTheme);

// Listen for theme toggle
document.getElementById('toggle_button').addEventListener('click', () => {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === THEMES.dark ? THEMES.light : THEMES.dark;
    setTheme(newTheme);
});


const fullScreenButton=document.getElementById('toggle_full_screen');
 fullScreenButton.addEventListener('click', () => {
 
    const content = document.getElementById('content');
    const rightpannel = document.getElementById('right-panel');
   
    const leftpannel = document.getElementById('left-panel');
    rightpannel.classList.add('s');
    if (rightpannel.classList.contains('fullscreen')) {
        rightpannel.classList.toggle('fullscreen');
        content.style.gridTemplateColumns = '1fr 1fr';
        leftpannel.style.display = 'flex';
        fullScreenButton.textContent='↗️'
    } else {
        rightpannel.classList.toggle('fullscreen');
        content.style.gridTemplateColumns = '1fr';
        leftpannel.style.display = 'none';
        fullScreenButton.textContent='❌'
    }

});