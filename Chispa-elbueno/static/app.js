const API_BASE = '/api';

async function apiCall(endpoint, method = 'GET', body = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json'
        }
    };
    if (body) {
        options.body = JSON.stringify(body);
    }
    const res = await fetch(`${API_BASE}${endpoint}`, options);
    if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Error en la solicitud');
    }
    return res.json();
}

// Modal Functions
function openPlanModal(button, planName) {
    const modal = document.getElementById('planModal');
    const title = document.getElementById('modalPlanName');
    const summaryContainer = document.querySelector('#modalPlanSummary .plan-features');
    
    if (modal && title) {
        title.innerText = planName;
        
        // Copiar las características del plan seleccionado
        if (summaryContainer && button) {
            const card = button.closest('.plan-card');
            if (card) {
                const features = card.querySelector('.plan-features');
                if (features) {
                    summaryContainer.innerHTML = features.innerHTML;
                }
            }
        }
        
        modal.style.display = 'flex';
    }
}

function closePlanModal() {
    const modal = document.getElementById('planModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

function sendToWhatsApp(event) {
    event.preventDefault();
    const planName = document.getElementById('modalPlanName').innerText;
    const userName = document.getElementById('userName').value;
    const userDuda = document.getElementById('userDuda').value;
    
    let message = `Hola, soy ${userName}. Me interesa el plan *${planName}*.`;
    if (userDuda) {
        message += `\nMi duda es: ${userDuda}`;
    }
    
    const phone = '525587989223'; // Número base
    const url = `https://wa.me/${phone}?text=${encodeURIComponent(message)}`;
    
    window.open(url, '_blank');
    closePlanModal();
}

window.onclick = function(event) {
    const modal = document.getElementById('planModal');
    if (event.target === modal) {
        closePlanModal();
    }
}
