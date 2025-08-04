// E-Store JavaScript

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Cart quantity update with AJAX
    const quantityInputs = document.querySelectorAll('input[name="quantity"]');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            const form = this.closest('form');
            if (form) {
                // Show loading state
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    const originalText = submitBtn.innerHTML;
                    submitBtn.innerHTML = '<span class="loading"></span>';
                    submitBtn.disabled = true;
                    
                    // Submit form
                    form.submit();
                }
            }
        });
    });

    // Add to cart with quantity validation
    const addToCartForms = document.querySelectorAll('form[action*="add-to-cart"]');
    addToCartForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const quantityInput = this.querySelector('input[name="quantity"]');
            if (quantityInput) {
                const quantity = parseInt(quantityInput.value);
                const maxStock = parseInt(quantityInput.getAttribute('max'));
                
                if (quantity > maxStock) {
                    e.preventDefault();
                    showAlert('Only ' + maxStock + ' items available in stock.', 'warning');
                    return false;
                }
                
                if (quantity <= 0) {
                    e.preventDefault();
                    showAlert('Please select a valid quantity.', 'warning');
                    return false;
                }
            }
        });
    });

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showAlert('Please fill in all required fields.', 'warning');
            }
        });
    });

    // Password confirmation validation
    const passwordForm = document.querySelector('form[action*="register"]');
    if (passwordForm) {
        const password1 = passwordForm.querySelector('#password1');
        const password2 = passwordForm.querySelector('#password2');
        
        if (password1 && password2) {
            password2.addEventListener('input', function() {
                if (password1.value !== this.value) {
                    this.setCustomValidity('Passwords do not match');
                    this.classList.add('is-invalid');
                } else {
                    this.setCustomValidity('');
                    this.classList.remove('is-invalid');
                }
            });
        }
    }

    // Search functionality
    const searchForm = document.querySelector('form[action*="product_list"]');
    if (searchForm) {
        const searchInput = searchForm.querySelector('input[name="search"]');
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                if (this.value.length >= 2 || this.value.length === 0) {
                    searchForm.submit();
                }
            }, 500);
        });
    }

    // Product image lazy loading
    const productImages = document.querySelectorAll('.card-img-top');
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        productImages.forEach(img => {
            if (img.dataset.src) {
                imageObserver.observe(img);
            }
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Cart item removal confirmation
    const removeButtons = document.querySelectorAll('form[action*="remove-from-cart"]');
    removeButtons.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!confirm('Are you sure you want to remove this item from your cart?')) {
                e.preventDefault();
            }
        });
    });

    // Profile picture preview
    const profilePictureInput = document.querySelector('input[name="profile_picture"]');
    if (profilePictureInput) {
        profilePictureInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const preview = document.querySelector('.profile-picture-preview');
                    if (preview) {
                        preview.src = e.target.result;
                        preview.style.display = 'block';
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // Checkout form enhancement
    const checkoutForm = document.querySelector('form[action*="checkout"]');
    if (checkoutForm) {
        const phoneInput = checkoutForm.querySelector('input[name="phone_number"]');
        if (phoneInput) {
            phoneInput.addEventListener('input', function() {
                // Remove non-numeric characters
                this.value = this.value.replace(/[^0-9]/g, '');
            });
        }
    }

    // Order status timeline animation
    const timelineItems = document.querySelectorAll('.timeline-item');
    if ('IntersectionObserver' in window) {
        const timelineObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateX(0)';
                }
            });
        }, { threshold: 0.5 });

        timelineItems.forEach(item => {
            item.style.opacity = '0';
            item.style.transform = 'translateX(-20px)';
            item.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            timelineObserver.observe(item);
        });
    }
});

// Utility function to show alerts
function showAlert(message, type = 'info') {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert alert-${type} alert-dismissible fade show`;
    alertContainer.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertContainer, container.firstChild);
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alertContainer);
            bsAlert.close();
        }, 5000);
    }
}

// Cart total calculation
function updateCartTotal() {
    const cartItems = document.querySelectorAll('.cart-item');
    let total = 0;
    
    cartItems.forEach(item => {
        const price = parseFloat(item.querySelector('.item-price').textContent.replace('₹', ''));
        const quantity = parseInt(item.querySelector('input[name="quantity"]').value);
        total += price * quantity;
    });
    
    const totalElement = document.querySelector('.cart-total');
    if (totalElement) {
        totalElement.textContent = '₹' + total.toFixed(2);
    }
}

// Product search with debouncing
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Initialize search functionality
const searchProducts = debounce(function(query) {
    if (query.length >= 2) {
        window.location.href = `/products/?search=${encodeURIComponent(query)}`;
    }
}, 500);

// Add event listener for search input
const searchInput = document.querySelector('input[name="search"]');
if (searchInput) {
    searchInput.addEventListener('input', function() {
        searchProducts(this.value);
    });
}
