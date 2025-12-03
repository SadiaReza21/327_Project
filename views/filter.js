// filter.js - UPDATED FOR YOUR FASTAPI BACKEND
document.addEventListener('DOMContentLoaded', function() {
    initFilterApp();
});

// Global state
let filterState = {
    categories: [],
    minPrice: 0,
    maxPrice: 100,
    searchQuery: '',
    sortBy: 'default',
    inStockOnly: true,
    cart: [],
    cartCount: 0
};

// Initialize application
function initFilterApp() {
    loadInitialData();
    setupEventListeners();
    updateCartCount();
}

// Load initial data from YOUR API
async function loadInitialData() {
    showLoading(true);
    
    try {
        // Load categories and products in parallel from YOUR API
        const [categories, productsResponse] = await Promise.all([
            fetchCategories(),
            fetchFilteredProducts()
        ]);
        
        filterState.categories = categories.map(cat => ({
            id: cat.id,
            name: cat.name,
            selected: true,
            icon: cat.icon
        }));
        
        populateCategories();
        displayProducts(productsResponse);
        updateResultsInfo(productsResponse.total_count || productsResponse.products?.length || 0, 'loaded');
        
        // Initialize price range
        const products = productsResponse.products || productsResponse || [];
        initializePriceSlider(products);
        
    } catch (error) {
        console.error('Failed to load initial data:', error);
        showErrorMessage('Failed to load products. Please try again.');
    } finally {
        showLoading(false);
    }
}

// Setup event listeners
function setupEventListeners() {
    // Sidebar toggle
    const hamburgerBtn = document.getElementById('hamburgerBtn');
    const closeBtn = document.getElementById('closeBtn');
    const filterToggleBtn = document.getElementById('filterToggleBtn');
    const overlay = document.getElementById('overlay');
    
    if (hamburgerBtn) hamburgerBtn.addEventListener('click', toggleSidebar);
    if (closeBtn) closeBtn.addEventListener('click', toggleSidebar);
    if (filterToggleBtn) filterToggleBtn.addEventListener('click', toggleSidebar);
    if (overlay) overlay.addEventListener('click', toggleSidebar);
    
    // Search
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                filterState.searchQuery = e.target.value.trim();
                applyFilters();
            }, 500);
        });
    }
    
    // Price slider
    const priceSlider = document.getElementById('priceSlider');
    if (priceSlider) {
        priceSlider.addEventListener('input', (e) => {
            const value = e.target.value;
            document.getElementById('maxPrice').value = value;
            filterState.maxPrice = parseInt(value);
            updateActiveFilters();
        });
    }
    
    // Price inputs
    const minPriceInput = document.getElementById('minPrice');
    const maxPriceInput = document.getElementById('maxPrice');
    
    if (minPriceInput) {
        minPriceInput.addEventListener('change', (e) => {
            filterState.minPrice = parseInt(e.target.value) || 0;
            applyFilters();
        });
    }
    
    if (maxPriceInput) {
        maxPriceInput.addEventListener('change', (e) => {
            filterState.maxPrice = parseInt(e.target.value) || 100;
            applyFilters();
        });
    }
    
    // Sort select
    const sortSelect = document.getElementById('sortSelect');
    if (sortSelect) {
        sortSelect.addEventListener('change', (e) => {
            filterState.sortBy = e.target.value;
            applyFilters();
        });
    }
    
    // In stock filter
    const inStockCheckbox = document.getElementById('inStockOnly');
    if (inStockCheckbox) {
        inStockCheckbox.addEventListener('change', (e) => {
            filterState.inStockOnly = e.target.checked;
            applyFilters();
        });
    }
    
    // Filter buttons
    const applyBtn = document.getElementById('applyFilters');
    const resetBtn = document.getElementById('resetFilters');
    const clearAllBtn = document.getElementById('clearAllFilters');
    const retryBtn = document.getElementById('retryBtn');
    
    if (applyBtn) applyBtn.addEventListener('click', applyFilters);
    if (resetBtn) resetBtn.addEventListener('click', resetFilters);
    if (clearAllBtn) clearAllBtn.addEventListener('click', resetFilters);
    if (retryBtn) retryBtn.addEventListener('click', loadInitialData);
    
    // View toggle
    const viewButtons = document.querySelectorAll('.view-btn');
    viewButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const view = e.target.dataset.view || e.target.closest('.view-btn').dataset.view;
            setViewMode(view);
        });
    });
    
    // Event delegation for dynamic elements
    document.addEventListener('click', (e) => {
        // Add to cart
        if (e.target.classList.contains('add-to-cart') || 
            e.target.closest('.add-to-cart')) {
            const button = e.target.classList.contains('add-to-cart') 
                ? e.target 
                : e.target.closest('.add-to-cart');
            const productId = button.dataset.productId;
            if (productId) handleAddToCart(productId);
        }
        
        // Remove filter tag
        if (e.target.classList.contains('remove-filter') || 
            e.target.closest('.remove-filter')) {
            const button = e.target.classList.contains('remove-filter') 
                ? e.target 
                : e.target.closest('.remove-filter');
            const filterType = button.dataset.filterType;
            const filterValue = button.dataset.filterValue;
            removeFilter(filterType, filterValue);
        }
        
        // Favorite toggle
        if (e.target.classList.contains('product-favorite') || 
            e.target.closest('.product-favorite')) {
            const button = e.target.classList.contains('product-favorite') 
                ? e.target 
                : e.target.closest('.product-favorite');
            toggleFavorite(button);
        }
    });
}

// Toggle sidebar
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');
    const hamburgerBtn = document.getElementById('hamburgerBtn');
    
    sidebar.classList.toggle('active');
    overlay.classList.toggle('active');
    
    if (hamburgerBtn) {
        const spans = hamburgerBtn.querySelectorAll('span');
        if (sidebar.classList.contains('active')) {
            spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
            spans[1].style.opacity = '0';
            spans[2].style.transform = 'rotate(-45deg) translate(7px, -6px)';
        } else {
            spans[0].style.transform = 'none';
            spans[1].style.opacity = '1';
            spans[2].style.transform = 'none';
        }
    }
}

// Fetch categories from YOUR API
async function fetchCategories() {
    try {
        const response = await fetch('/api/v1/filter/categories');
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        const categories = await response.json();
        // Convert string categories to objects with icons
        return categories.map(categoryName => ({
            id: categoryName.toLowerCase().replace(/\s+/g, '_'),
            name: categoryName,
            icon: getCategoryIcon(categoryName)
        }));
    } catch (error) {
        console.error('Error fetching categories:', error);
        // Return default categories if API fails
        return [
            { id: 'fruits', name: 'Fruits', icon: 'fas fa-apple-alt' },
            { id: 'vegetables', name: 'Vegetables', icon: 'fas fa-carrot' },
            { id: 'dairy', name: 'Dairy', icon: 'fas fa-egg' },
            { id: 'bakery', name: 'Bakery', icon: 'fas fa-bread-slice' },
            { id: 'meat', name: 'Meat', icon: 'fas fa-drumstick-bite' },
            { id: 'grains', name: 'Grains', icon: 'fas fa-seedling' },
            { id: 'beverages', name: 'Beverages', icon: 'fas fa-wine-bottle' }
        ];
    }
}

// Fetch filtered products from YOUR API
async function fetchFilteredProducts() {
    try {
        // Build query parameters for YOUR API
        const params = new URLSearchParams();
        
        // Get selected categories
        const selectedCategories = filterState.categories
            .filter(cat => cat.selected)
            .map(cat => cat.name);
        
        if (selectedCategories.length > 0) {
            // For now, send first category (your API supports single category)
            params.append('category', selectedCategories[0]);
        }
        
        if (filterState.minPrice > 0) {
            params.append('min_price', filterState.minPrice);
        }
        
        if (filterState.maxPrice < 100) {
            params.append('max_price', filterState.maxPrice);
        }
        
        if (filterState.searchQuery) {
            params.append('search', filterState.searchQuery);
        }
        
        if (filterState.sortBy !== 'default') {
            params.append('sort', filterState.sortBy);
        }
        
        const apiUrl = `/api/v1/filter?${params.toString()}`;
        console.log('Fetching from API:', apiUrl);
        
        const response = await fetch(apiUrl);
        
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP ${response.status}: ${errorText}`);
        }
        
        return await response.json();
        
    } catch (error) {
        console.error('Error fetching filtered products:', error);
        throw error;
    }
}

// Helper function to get icon for category
function getCategoryIcon(categoryName) {
    const iconMap = {
        'Fruits': 'fas fa-apple-alt',
        'Vegetables': 'fas fa-carrot',
        'Dairy': 'fas fa-egg',
        'Bakery': 'fas fa-bread-slice',
        'Meat': 'fas fa-drumstick-bite',
        'Grains': 'fas fa-seedling',
        'Beverages': 'fas fa-wine-bottle'
    };
    return iconMap[categoryName] || 'fas fa-tag';
}

// Populate categories in sidebar
function populateCategories() {
    const container = document.getElementById('categoriesContainer');
    if (!container) return;
    
    container.innerHTML = '';
    
    // Get unique categories from state
    const uniqueCategories = [...new Set(filterState.categories.map(c => c.name))];
    
    uniqueCategories.forEach(categoryName => {
        const category = filterState.categories.find(c => c.name === categoryName);
        const isSelected = category ? category.selected : true;
        const icon = category ? category.icon : getCategoryIcon(categoryName);
        
        const checkbox = document.createElement('label');
        checkbox.className = 'checkbox-label';
        
        checkbox.innerHTML = `
            <input type="checkbox" 
                   ${isSelected ? 'checked' : ''}
                   data-category="${categoryName}">
            <span class="checkmark"></span>
            <i class="${icon}"></i>
            ${categoryName}
        `;
        
        checkbox.querySelector('input').addEventListener('change', (e) => {
            const catName = e.target.dataset.category;
            const categoryObj = filterState.categories.find(c => c.name === catName);
            if (categoryObj) {
                categoryObj.selected = e.target.checked;
            } else {
                filterState.categories.push({
                    name: catName, 
                    selected: e.target.checked,
                    icon: getCategoryIcon(catName)
                });
            }
            applyFilters();
        });
        
        container.appendChild(checkbox);
    });
}

// Display products
function displayProducts(productsResponse) {
    const container = document.getElementById('productsGrid');
    if (!container) return;
    
    container.innerHTML = '';
    
    // Check if productsResponse has products property
    const products = productsResponse.products || productsResponse;
    
    if (!products || products.length === 0) {
        document.getElementById('noResultsMessage').classList.remove('hidden');
        document.getElementById('productsGrid').classList.add('hidden');
        return;
    }
    
    document.getElementById('noResultsMessage').classList.add('hidden');
    document.getElementById('productsGrid').classList.remove('hidden');
    
    products.forEach(product => {
        const productCard = createProductCard(product);
        container.appendChild(productCard);
    });
}

// Create product card for YOUR data structure
function createProductCard(product) {
    const card = document.createElement('div');
    card.className = 'product-card';
    
    // Map category to icon for placeholder
    const categoryIconMap = {
        'Fruits': 'fas fa-apple-alt',
        'Vegetables': 'fas fa-carrot',
        'Dairy': 'fas fa-egg',
        'Bakery': 'fas fa-bread-slice',
        'Meat': 'fas fa-drumstick-bite',
        'Grains': 'fas fa-seedling',
        'Beverages': 'fas fa-wine-bottle'
    };
    
    const iconClass = categoryIconMap[product.category] || 'fas fa-shopping-basket';
    
    // Stock status
    const stockQuantity = product.stock_quantity || 0;
    const isAvailable = product.is_available !== false;
    
    let stockClass = 'stock-available';
    let stockText = 'In Stock';
    let isOutOfStock = false;
    
    if (!isAvailable || stockQuantity === 0) {
        stockClass = 'stock-out';
        stockText = 'Out of Stock';
        isOutOfStock = true;
    } else if (stockQuantity < 10) {
        stockClass = 'stock-low';
        stockText = `Low Stock (${stockQuantity})`;
    } else {
        stockText = `In Stock (${stockQuantity})`;
    }
    
    // Generate a random rating for demo (3.0 to 5.0 stars)
    const rating = (Math.random() * 2 + 3).toFixed(1);
    const stars = Math.round(rating);
    
    let starsHTML = '';
    for (let i = 1; i <= 5; i++) {
        starsHTML += `<i class="fas fa-star${i <= stars ? '' : '-o'}"></i>`;
    }
    
    card.innerHTML = `
        <div class="product-image">
            ${product.image_url && product.image_url.startsWith('http') 
                ? `<img src="${product.image_url}" alt="${product.name}" onerror="this.onerror=null; this.style.display='none'; this.parentElement.innerHTML='<i class=\\'${iconClass} image-placeholder\\'></i>';">`
                : `<i class="${iconClass} image-placeholder"></i>`
            }
            <span class="product-badge">${product.category}</span>
        </div>
        <div class="product-info">
            <div class="product-header">
                <h3 class="product-name">${product.name}</h3>
                <button class="product-favorite" aria-label="Add to favorites">
                    <i class="far fa-heart"></i>
                </button>
            </div>
            <p class="product-category">
                <i class="fas fa-tag"></i> ${product.category}
            </p>
            <div class="product-rating">
                ${starsHTML}
                <span class="rating-text">${rating}</span>
            </div>
            <p class="product-description">${product.description}</p>
            <div class="product-footer">
                <div>
                    <div class="product-price">$${product.price.toFixed(2)}</div>
                    <div class="price-unit">per ${getUnitForProduct(product.name)}</div>
                </div>
                <span class="product-stock ${stockClass}">${stockText}</span>
            </div>
            <button class="add-to-cart" 
                    data-product-id="${product.product_id || product.name}"
                    ${isOutOfStock ? 'disabled' : ''}>
                <i class="fas fa-shopping-cart"></i>
                ${isOutOfStock ? 'Out of Stock' : 'Add to Cart'}
            </button>
        </div>
    `;
    
    return card;
}

// Helper: Get unit based on product name
function getUnitForProduct(productName) {
    const name = productName.toLowerCase();
    if (name.includes('milk') || name.includes('juice')) return 'gallon';
    if (name.includes('eggs')) return 'dozen';
    if (name.includes('rice')) return 'bag';
    if (name.includes('chicken')) return 'lb';
    if (name.includes('bread')) return 'loaf';
    return 'item';
}

// Apply filters
async function applyFilters() {
    showLoading(true);
    updateActiveFilters();
    
    try {
        const response = await fetchFilteredProducts();
        displayProducts(response);
        updateResultsInfo(response.total_count || response.products?.length || 0, 'filtered');
    } catch (error) {
        console.error('Error applying filters:', error);
        showErrorMessage('Failed to apply filters. Please try again.');
    } finally {
        showLoading(false);
    }
}

// Reset filters
function resetFilters() {
    // Reset category selections
    filterState.categories.forEach(cat => cat.selected = true);
    
    // Reset other filters
    filterState.minPrice = 0;
    filterState.maxPrice = 100;
    filterState.searchQuery = '';
    filterState.sortBy = 'default';
    filterState.inStockOnly = true;
    
    // Update UI
    document.getElementById('searchInput').value = '';
    document.getElementById('minPrice').value = '0';
    document.getElementById('maxPrice').value = '100';
    document.getElementById('priceSlider').value = '100';
    document.getElementById('sortSelect').value = 'default';
    document.getElementById('inStockOnly').checked = true;
    
    populateCategories();
    applyFilters();
}

// Remove specific filter
function removeFilter(type, value) {
    switch (type) {
        case 'category':
            const category = filterState.categories.find(c => c.name === value);
            if (category) category.selected = false;
            break;
        case 'search':
            filterState.searchQuery = '';
            document.getElementById('searchInput').value = '';
            break;
        case 'price':
            filterState.minPrice = 0;
            filterState.maxPrice = 100;
            document.getElementById('minPrice').value = '0';
            document.getElementById('maxPrice').value = '100';
            document.getElementById('priceSlider').value = '100';
            break;
    }
    
    populateCategories();
    applyFilters();
}

// Update active filters display
function updateActiveFilters() {
    const container = document.getElementById('activeFilters');
    if (!container) return;
    
    container.innerHTML = '';
    
    // Selected categories (only show if some are unselected)
    const selectedCategories = filterState.categories.filter(cat => cat.selected);
    const allCategories = filterState.categories.length;
    
    if (selectedCategories.length < allCategories) {
        selectedCategories.forEach(cat => {
            const tag = document.createElement('span');
            tag.className = 'filter-tag';
            tag.innerHTML = `
                <i class="fas fa-tag"></i> ${cat.name}
                <button class="remove remove-filter" 
                        data-filter-type="category" 
                        data-filter-value="${cat.name}">×</button>
            `;
            container.appendChild(tag);
        });
    }
    
    // Price filter
    if (filterState.minPrice > 0 || filterState.maxPrice < 100) {
        const tag = document.createElement('span');
        tag.className = 'filter-tag';
        tag.innerHTML = `
            <i class="fas fa-dollar-sign"></i> 
            $${filterState.minPrice} - $${filterState.maxPrice}
            <button class="remove remove-filter" 
                    data-filter-type="price">×</button>
        `;
        container.appendChild(tag);
    }
    
    // Search query
    if (filterState.searchQuery) {
        const tag = document.createElement('span');
        tag.className = 'filter-tag';
        tag.innerHTML = `
            <i class="fas fa-search"></i> "${filterState.searchQuery}"
            <button class="remove remove-filter" 
                    data-filter-type="search">×</button>
        `;
        container.appendChild(tag);
    }
}

// Update results info
function updateResultsInfo(count, action) {
    const countElement = document.getElementById('resultsCount');
    const titleElement = document.getElementById('resultsTitle');
    const timeElement = document.getElementById('resultsTime');
    
    if (countElement) {
        countElement.textContent = `${count} product${count !== 1 ? 's' : ''}`;
    }
    
    if (titleElement) {
        if (action === 'filtered' && (filterState.searchQuery || filterState.minPrice > 0 || filterState.maxPrice < 100)) {
            titleElement.textContent = 'Filtered Products';
        } else {
            titleElement.textContent = 'All Products';
        }
    }
    
    if (timeElement) {
        const now = new Date();
        timeElement.textContent = `Last updated: ${now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}`;
    }
}

// Initialize price slider
function initializePriceSlider(products) {
    const slider = document.getElementById('priceSlider');
    const maxPriceInput = document.getElementById('maxPrice');
    
    if (slider && products && products.length > 0) {
        const prices = products.map(p => p.price || 0);
        const maxPrice = Math.max(...prices);
        const roundedMax = Math.ceil(maxPrice / 10) * 10;
        
        slider.max = roundedMax || 100;
        slider.value = slider.max;
        maxPriceInput.placeholder = slider.max;
        filterState.maxPrice = slider.max;
        maxPriceInput.value = slider.max;
    }
}

// Set view mode
function setViewMode(mode) {
    const container = document.getElementById('productsGrid');
    const viewButtons = document.querySelectorAll('.view-btn');
    
    viewButtons.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.view === mode);
    });
    
    container.className = `products-grid ${mode}-view`;
}

// Handle add to cart
function handleAddToCart(productId) {
    // For now, just increment cart count
    filterState.cartCount++;
    updateCartCount();
    showCartNotification();
    
    // In a real app, you would:
    // 1. Send to backend API
    // 2. Update cart with actual product
    console.log('Added product to cart:', productId);
}

// Update cart count
function updateCartCount() {
    const countElements = document.querySelectorAll('.cart-count');
    
    countElements.forEach(el => {
        el.textContent = filterState.cartCount;
    });
}

// Show cart notification
function showCartNotification() {
    const notification = document.getElementById('cartNotification');
    notification.classList.remove('hidden');
    notification.classList.add('show');
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.classList.add('hidden');
        }, 300);
    }, 2000);
}

// Toggle favorite
function toggleFavorite(button) {
    const icon = button.querySelector('i');
    const isActive = button.classList.contains('active');
    
    if (isActive) {
        button.classList.remove('active');
        icon.className = 'far fa-heart';
    } else {
        button.classList.add('active');
        icon.className = 'fas fa-heart';
    }
}

// Show loading
function showLoading(show) {
    const spinner = document.getElementById('loadingSpinner');
    const productsGrid = document.getElementById('productsGrid');
    
    if (show) {
        spinner.classList.remove('hidden');
        if (productsGrid) productsGrid.classList.add('loading');
    } else {
        spinner.classList.add('hidden');
        if (productsGrid) productsGrid.classList.remove('loading');
    }
}

// Show error message
function showErrorMessage(message = 'An error occurred. Please try again.') {
    const errorElement = document.getElementById('errorMessage');
    if (errorElement) {
        errorElement.querySelector('h3').nextElementSibling.textContent = message;
        errorElement.classList.remove('hidden');
    }
}

// Initialize price range on load
window.addEventListener('load', () => {
    // Set initial price range
    const minPriceInput = document.getElementById('minPrice');
    const maxPriceInput = document.getElementById('maxPrice');
    const priceSlider = document.getElementById('priceSlider');
    
    if (minPriceInput) minPriceInput.value = '0';
    if (maxPriceInput) maxPriceInput.value = '100';
    if (priceSlider) priceSlider.value = '100';
});