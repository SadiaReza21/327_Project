
document.addEventListener('DOMContentLoaded', function() {
    // Initialize when DOM is fully loaded
    loadInitialCategoriesAndProducts();
    setupEventListeners();
});

async function loadInitialCategoriesAndProducts() {
    try {
        const [categories, products] = await Promise.all([
            fetchCategories(),
            fetchAllProducts()
        ]);
        populateCategories(categories);
        displayProducts(products);
        updateResultsHeader('All Products', products.length);
    } catch (error) {
        console.error('Failed to load initial data:', error);
        showErrorMessage();
    }
}

function setupEventListeners() {
    // Category filter event listeners
    const categoryFilters = document.querySelectorAll('.category-filter');
    categoryFilters.forEach(filter => {
        filter.addEventListener('change', handleCategoryFilter);
    });

    // Search functionality
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', handleSearch);
    }

    // Price range filters
    const priceMin = document.getElementById('price-min');
    const priceMax = document.getElementById('price-max');
    if (priceMin && priceMax) {
        priceMin.addEventListener('change', handlePriceFilter);
        priceMax.addEventListener('change', handlePriceFilter);
    }

    // Sort functionality
    const sortSelect = document.getElementById('sort-select');
    if (sortSelect) {
        sortSelect.addEventListener('change', handleSort);
    }

    const applyBtn = document.getElementById('applyFilters');
    const resetBtn = document.getElementById('resetFilters');
    const categorySelect = document.getElementById('categoryFilter');
    const minPrice = document.getElementById('minPrice');
    const maxPrice = document.getElementById('maxPrice');

    if (applyBtn) applyBtn.addEventListener('click', applyFilterFromSidebar);
    if (resetBtn) resetBtn.addEventListener('click', resetFilterFromSidebar);
    if (categorySelect) categorySelect.addEventListener('change', applyFilterFromSidebar);
    if (minPrice) minPrice.addEventListener('keypress', e => e.key === 'Enter' && applyFilterFromSidebar());
    if (maxPrice) maxPrice.addEventListener('keypress', e => e.key === 'Enter' && applyFilterFromSidebar());
}
async function fetchCategories() {
    try {
        const response = await fetch('/api/categories');
        if (!response.ok) {
            throw new Error('Failed to fetch categories');
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching categories:', error);
        throw error;
    }
}

async function fetchAllProducts() {
    try {
        const response = await fetch('/api/products');
        if (!response.ok) {
            throw new Error('Failed to fetch products');
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching products:', error);
        throw error;
    }
}

async function fetchFilteredProducts(filters) {
    try {
        const queryParams = new URLSearchParams(filters).toString();
        const response = await fetch(`/api/products/filter?${queryParams}`);
        if (!response.ok) {
            throw new Error('Failed to fetch filtered products');
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching filtered products:', error);
        throw error;
    }
}

function populateCategories(categories) {
    const categoriesContainer = document.getElementById('categories-container');
    if (!categoriesContainer) return;

    categoriesContainer.innerHTML = '';
    
    categories.forEach(category => {
        const categoryElement = document.createElement('div');
        categoryElement.className = 'category-item';
        categoryElement.innerHTML = `
            <input type="checkbox" 
                   class="category-filter" 
                   value="${category.id}" 
                   id="category-${category.id}">
            <label for="category-${category.id}">${category.name}</label>
        `;
        categoriesContainer.appendChild(categoryElement);
    });

    // Re-attach event listeners after populating
    const categoryFilters = document.querySelectorAll('.category-filter');
    categoryFilters.forEach(filter => {
        filter.addEventListener('change', handleCategoryFilter);
    });
}

function displayProducts(products) {
    const productsContainer = document.getElementById('products-container');
    if (!productsContainer) return;

    productsContainer.innerHTML = '';

    if (products.length === 0) {
        productsContainer.innerHTML = '<p class="no-products">No products found.</p>';
        return;
    }

    products.forEach(product => {
        const productElement = document.createElement('div');
        productElement.className = 'product-card';
        productElement.innerHTML = `
            <img src="${product.image || '/images/placeholder.jpg'}" 
                 alt="${product.name}" 
                 class="product-image">
            <h3 class="product-name">${product.name}</h3>
            <p class="product-price">$${product.price.toFixed(2)}</p>
            <p class="product-category">${product.category}</p>
            <button class="add-to-cart" data-product-id="${product.id}">
                Add to Cart
            </button>
        `;
        productsContainer.appendChild(productElement);
    });

    // Add event listeners to add-to-cart buttons
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', handleAddToCart);
    });
}

function updateResultsHeader(category, count) {
    const resultsHeader = document.getElementById('results-header');
    if (resultsHeader) {
        resultsHeader.textContent = `${category} (${count} products)`;
    }
}

async function handleCategoryFilter() {
    const selectedCategories = Array.from(document.querySelectorAll('.category-filter:checked'))
        .map(checkbox => checkbox.value);

    try {
        const filters = {
            categories: selectedCategories.join(',')
        };
        
        const products = await fetchFilteredProducts(filters);
        displayProducts(products);
        updateResultsHeader('Filtered Products', products.length);
    } catch (error) {
        console.error('Error filtering products by category:', error);
        showErrorMessage();
    }
}

async function handleSearch(event) {
    const searchTerm = event.target.value.trim();
    
    if (searchTerm.length < 2 && searchTerm.length > 0) {
        return; // Wait for at least 2 characters
    }

    try {
        const filters = {};
        if (searchTerm) {
            filters.search = searchTerm;
        }

        // Also include selected categories
        const selectedCategories = Array.from(document.querySelectorAll('.category-filter:checked'))
            .map(checkbox => checkbox.value);
        if (selectedCategories.length > 0) {
            filters.categories = selectedCategories.join(',');
        }

        const products = await fetchFilteredProducts(filters);
        displayProducts(products);
        updateResultsHeader(searchTerm ? `Search: ${searchTerm}` : 'All Products', products.length);
    } catch (error) {
        console.error('Error searching products:', error);
        showErrorMessage();
    }
}

async function handlePriceFilter() {
    const priceMin = document.getElementById('price-min').value;
    const priceMax = document.getElementById('price-max').value;

    try {
        const filters = {};
        
        if (priceMin) filters.minPrice = priceMin;
        if (priceMax) filters.maxPrice = priceMax;

        // Include selected categories
        const selectedCategories = Array.from(document.querySelectorAll('.category-filter:checked'))
            .map(checkbox => checkbox.value);
        if (selectedCategories.length > 0) {
            filters.categories = selectedCategories.join(',');
        }

        const products = await fetchFilteredProducts(filters);
        displayProducts(products);
        updateResultsHeader('Filtered Products', products.length);
    } catch (error) {
        console.error('Error filtering products by price:', error);
        showErrorMessage();
    }
}

async function handleSort(event) {
    const sortBy = event.target.value;
    
    try {
        const filters = { sort: sortBy };

        // Include selected categories
        const selectedCategories = Array.from(document.querySelectorAll('.category-filter:checked'))
            .map(checkbox => checkbox.value);
        if (selectedCategories.length > 0) {
            filters.categories = selectedCategories.join(',');
        }

        const products = await fetchFilteredProducts(filters);
        displayProducts(products);
        updateResultsHeader('Sorted Products', products.length);
    } catch (error) {
        console.error('Error sorting products:', error);
        showErrorMessage();
    }
}

function handleAddToCart(event) {
    const productId = event.target.getAttribute('data-product-id');
    
    // Add to cart logic here
    console.log(`Adding product ${productId} to cart`);
    
    //  implementing add to cart functionality here
    ;
}

function showErrorMessage(message = 'An error occurred. Please try again.') {
    // Implement error message display
    const errorDiv = document.getElementById('error-message') || createErrorMessageElement();
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}

function createErrorMessageElement() {
    const errorDiv = document.createElement('div');
    errorDiv.id = 'error-message';
    errorDiv.className = 'error-message';
    errorDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #f44336;
        color: white;
        padding: 15px;
        border-radius: 5px;
        z-index: 1000;
        display: none;
    `;
    document.body.appendChild(errorDiv);
    return errorDiv;
}

// Export functions if using modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        loadInitialCategoriesAndProducts,
        fetchCategories,
        fetchAllProducts,
        fetchFilteredProducts,
        populateCategories,
        displayProducts,
        updateResultsHeader
    };
}