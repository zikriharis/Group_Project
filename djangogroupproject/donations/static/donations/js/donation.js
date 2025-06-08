// Donation form functionality
function setAmount(amount) {
    document.getElementById('amount').value = amount;
    
    // Remove active class from all buttons
    document.querySelectorAll('.amount-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Add active class to clicked button
    event.target.classList.add('active');
}

// Form validation
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.donation-form');
    const amountInput = document.getElementById('amount');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            const amount = parseFloat(amountInput.value);
            
            if (amount < 5) {
                e.preventDefault();
                alert('Minimum donation amount is RM 5.00');
                amountInput.focus();
            }
        });
    }
    
    // Clear active buttons when typing custom amount
    if (amountInput) {
        amountInput.addEventListener('input', function() {
            document.querySelectorAll('.amount-btn').forEach(btn => {
                btn.classList.remove('active');
            });
        });
    }
});