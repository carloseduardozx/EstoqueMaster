// static/js/notifications.js

document.addEventListener('DOMContentLoaded', function() {
    // Pega as mensagens diretamente da variável global que criamos no layout.html
    const messages = window.flaskMessages || []; // O '|| []' é uma segurança

    // Se não houver mensagens, não faz nada
    if (messages.length === 0) {
        return;
    }

    const container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);

    messages.forEach(function(msg) {
        // msg já é um objeto {category: '...', message: '...'}
        const toast = document.createElement('div');
        toast.className = `toast toast-${msg[0]}`; // msg[0] é a categoria
        toast.textContent = msg[1]; // msg[1] é a mensagem

        container.appendChild(toast);

        setTimeout(() => {
            toast.classList.add('show');
        }, 100);

        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => {
                toast.remove();
            }, 500);
        }, 5000);
    });
});