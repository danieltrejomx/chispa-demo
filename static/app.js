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
function openPlanModal(button, planName, price) {
    const modal = document.getElementById('planModal');
    const title = document.getElementById('modalPlanName');
    const priceEl = document.getElementById('modalPlanPrice');
    const summaryContainer = document.querySelector('#modalPlanSummary .plan-features');
    
    if (modal && title) {
        title.innerText = planName;
        if (priceEl && price !== undefined) {
            priceEl.innerText = `$${price.toLocaleString('es-MX')} MXN`;
        }
        
        const planForm = document.getElementById('planForm');
        const paymentSuccess = document.getElementById('paymentSuccess');
        if(planForm) planForm.style.display = 'block';
        if(paymentSuccess) paymentSuccess.style.display = 'none';
        
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

function processPayment(event) {
    event.preventDefault();
    const btn = document.getElementById('payButton');
    if (!btn) return;
    
    const originalText = btn.innerHTML;
    
    btn.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Procesando...';
    btn.disabled = true;
    
    setTimeout(() => {
        btn.innerHTML = originalText;
        btn.disabled = false;
        document.getElementById('planForm').style.display = 'none';
        document.getElementById('paymentSuccess').style.display = 'block';
    }, 2000);
}

window.onclick = function(event) {
    const modal = document.getElementById('planModal');
    if (event.target === modal) {
        closePlanModal();
    }
}
