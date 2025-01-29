const THEMES = {
    light: 'light',
    dark: 'dark'
};
function setTheme(theme){
    document.documentElement.setAttribute('data-theme',theme);
    localStorage.setItem('theme', theme);
    const themeToggle=document.getElementById('theme-toggle');
    themeToggle.innerHTML=theme===THEMES.dark?'🔆':'🌙';
}
document.getElementById('theme-toggle').addEventListener('click',()=>{
    const theme=document.documentElement.getAttribute('data-theme');
    const newTheme=theme===THEMES.dark?THEMES.light:THEMES.dark;
    setTheme(newTheme);
})
const savedTheme=localStorage.getItem('theme')||THEMES.dark;
setTheme(savedTheme);


function viewprofile(){
    document.getElementById('profile-info-content').style.display='block';
    const profileInfo=document.getElementById('profile-info');
    profileInfo.classList.toggle('show');
         
}
function closeProfile(){
    const profileInfo=document.getElementById('profile-info');
    profileInfo.classList.toggle('show');
    document.getElementById('profile-info-content').style.display='none';  
    
}