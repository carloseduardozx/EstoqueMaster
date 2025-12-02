// static/js/theme-toggle.js

document.addEventListener('DOMContentLoaded', function() {
    const themeToggleButton = document.getElementById('theme-toggle');
    const body = document.body;

    // Função para aplicar o tema
    function applyTheme(theme) {
        if (theme === 'dark') {
            body.classList.add('dark-mode');
            themeToggleButton.innerHTML = '<i class="bi bi-sun-fill"></i>';
        } else {
            body.classList.remove('dark-mode');
            themeToggleButton.innerHTML = '<i class="bi bi-moon-stars-fill"></i>';
        }
    }

    // Verifica a preferência salva no localStorage ou a preferência do sistema
    const currentTheme = localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    applyTheme(currentTheme);

    // Adiciona o evento de clique no botão
    if (themeToggleButton) {
        themeToggleButton.addEventListener('click', function() {
            const newTheme = body.classList.contains('dark-mode') ? 'light' : 'dark';
            applyTheme(newTheme);
            localStorage.setItem('theme', newTheme);
        });
    }
});