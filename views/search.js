// Constants
const API_BASE_URL = 'http://localhost:8000';
const SEARCH_ENDPOINT = '/api/v1/search';
const PRODUCTS_ENDPOINT = '/api/v1/products';
const CATEGORIES_ENDPOINT = '/api/v1/categories';
const DEBOUNCE_DELAY = 500;


// MVC View Controller
class SearchView {
    
    constructor() {
        this.search_form_element = document.getElementById('searchForm');
        this.search_input_element = document.getElementById('searchInput');
        this.search_button_element = document.getElementById('searchButton');
        this.category_filter_element = document.getElementById('categoryFilter');
        this.min_price_element = document.getElementById('minPrice');
        this.max_price_element = document.getElementById('maxPrice');
        this.apply_filters_button = document.getElementById('applyFilters');
        this.reset_filters_button = document.getElementById('resetFilters');
        this.loading_spinner_element = document.getElementById('loadingSpinner');
        this.no_results_message_element = document.getElementById('noResultsMessage');
        this.empty_search_message_element = document.getElementById('emptySearchMessage');
        this.error_message_element = document.getElementById('errorMessage');
        this.products_grid_element = document.getElementById('productsGrid');
        
        this.current_search_query = '';
        this.current_category_filter = '';
        this.current_min_price = null;
        this.current_max_price = null;
        this.search_timeout_id = null;
    }
    
    
    fun_initialize_event_listeners(controller) {
        this.search_form_element.addEventListener('submit', (event) => {
            event.preventDefault();
            controller.fun_handle_search_submit();
        });
        
        this.search_input_element.addEventListener('input', (event) => {
            controller.fun_handle_search_input(event.target.value);
        });
        
        this.apply_filters_button.addEventListener('click', () => {
            controller.fun_apply_filters();
        });
        
        this.reset_filters_button.addEventListener('click', () => {
            controller.fun_reset_filters();
        });
    }
    
    
    fun_show_loading_spinner() {
        this.fun_hide_all_messages();
        this.loading_spinner_element.classList.remove('hidden');
        this.products_grid_element.innerHTML = '';
    }
    
    
    fun_hide_loading_spinner() {
        this.loading_spinner_element.classList.add('hidden');
    }
    
    
    fun_show_no_results_message() {
        this.fun_hide_all_messages();
        this.no_results_message_element.classList.remove('hidden');
        this.products_grid_element.innerHTML = '';
    }
    
    
    fun_show_empty_search_message() {
        this.fun_hide_all_messages();
        this.empty_search_message_element.classList.remove('hidden');
        this.products_grid_element.innerHTML = '';
    }
    
    
    fun_show_error_message() {
        this.fun_hide_all_messages();
        this.error_message_element.classList.remove('hidden');
        this.products_grid_element.innerHTML = '';
    }
    
    
    fun_hide_all_messages() {
        this.loading_spinner_element.classList.add('hidden');
        this.no_results_message_element.classList.add('hidden');
        this.empty_search_message_element.classList.add('hidden');
        this.error_message_element.classList.add('hidden');
    }
    
    
    fun_display_products(products_array) {
        if (!Array.isArray(products_array) || products_array.length === 0) {
            this.fun_show_no_results_message();
            return;
        }
        
        const products_html = products_array.map(product => 
            this.fun_create_product_card(product)
        ).join('');
        
        this.products_grid_element.innerHTML = products_html;
        this.fun_hide_all_messages();
    }
    
    
    fun_create_product_card(product_data) {
        const stock_status_class = product_data.stock_quantity > 10 ? 'stock-available' : 'stock-low';
        const stock_status_text = product_data.stock_quantity > 10 ? 'In Stock' : 'Low Stock';
        
        return `
            <div class="product-card" data-product-id="${product_data.product_id}">
                <div class="product-image">
                    ${product_data.image_url ? 
                        `<img src="${product_data.image_url}" alt="${product_data.name}" loading="lazy">` : 
                        '📱'
                    }
                </div>
                <div class="product-info">
                    <h3 class="product-name">${this.fun_escape_html(product_data.name)}</h3>
                    <p class="product-category">${this.fun_escape_html(product_data.category)}</p>
                    <p class="product-price">$${product_data.price.toFixed(2)}</p>
                    <span class="product-stock ${stock_status_class}">${stock_status_text}</span>
                    <p class="product-description">${this.fun_escape_html(product_data.description)}</p>
                </div>
            </div>
        `;
    }
    
    
    fun_populate_categories(categories_array) {
        const category_options = categories_array.map(category => 
            `<option value="${this.fun_escape_html(category)}">${this.fun_escape_html(category)}</option>`
        ).join('');
        
        this.category_filter_element.innerHTML = 
            '<option value="">All Categories</option>' + category_options;
    }
    
    
    fun_get_search_filters() {
        return {
            query: this.search_input_element.value.trim(),
            category: this.category_filter_element.value,
            min_price: this.min_price_element.value ? parseFloat(this.min_price_element.value) : null,
            max_price: this.max_price_element.value ? parseFloat(this.max_price_element.value) : null
        };
    }
    
    
    fun_update_search_state(filters) {
        this.current_search_query = filters.query;
        this.current_category_filter = filters.category;
        this.current_min_price = filters.min_price;
        this.current_max_price = filters.max_price;
    }
    
    
    fun_reset_filters_ui() {
        this.category_filter_element.value = '';
        this.min_price_element.value = '';
        this.max_price_element.value = '';
    }
    
    
    fun_clear_search_timeout() {
        if (this.search_timeout_id) {
            clearTimeout(this.search_timeout_id);
            this.search_timeout_id = null;
        }
    }
    
    
    fun_set_search_timeout(callback, delay) {
        this.search_timeout_id = setTimeout(callback, delay);
    }
    
    
    fun_escape_html(unsafe_text) {
        const text_area_element = document.createElement('textarea');
        text_area_element.textContent = unsafe_text;
        return text_area_element.innerHTML;
    }
}


// MVC Controller
class SearchController {
    
    constructor(view, api_service) {
        this.view = view;
        this.api_service = api_service;
        this.is_initialized = false;
    }
    
    
    async fun_initialize() {
        if (this.is_initialized) return;
        
        this.view.fun_initialize_event_listeners(this);
        await this.fun_load_initial_data();
        this.is_initialized = true;
        
        console.log('Search Controller initialized');
    }
    
    
    async fun_load_initial_data() {
        try {
            const [categories, products] = await Promise.all([
                this.api_service.fun_fetch_categories(),
                this.api_service.fun_fetch_all_products()
            ]);
            
            this.view.fun_populate_categories(categories);
            this.view.fun_display_products(products);
            
        } catch (error) {
            console.error('Failed to load initial data:', error);
            this.view.fun_show_error_message();
        }
    }
    
    
    fun_handle_search_submit() {
        this.view.fun_clear_search_timeout();
        this.fun_execute_search();
    }
    
    
    fun_handle_search_input(search_term) {
        this.view.fun_clear_search_timeout();
        
        if (search_term.length === 0) {
            this.view.fun_show_empty_search_message();
            return;
        }
        
        if (search_term.length < 2) {
            return;
        }
        
        this.view.fun_set_search_timeout(() => {
            this.fun_execute_search();
        }, DEBOUNCE_DELAY);
    }
    
    
    fun_apply_filters() {
        const filters = this.view.fun_get_search_filters();
        this.view.fun_update_search_state(filters);
        
        if (filters.query || filters.category) {
            this.fun_execute_search();
        }
    }
    
    
    async fun_execute_search() {
        const filters = this.view.fun_get_search_filters();
        
        if (!filters.query && !filters.category) {
            this.view.fun_show_empty_search_message();
            return;
        }
        
        this.view.fun_show_loading_spinner();
        
        try {
            const search_results = await this.api_service.fun_search_products(filters);
            this.view.fun_display_products(search_results.products);
            
        } catch (error) {
            console.error('Search error:', error);
            this.view.fun_show_error_message();
        } finally {
            this.view.fun_hide_loading_spinner();
        }
    }
    
    
    fun_reset_filters() {
        this.view.fun_reset_filters_ui();
        this.fun_execute_search();
    }
}


// API Service Layer
class ApiService {
    
    async fun_search_products(filters) {
        const search_params = new URLSearchParams();
        
        if (filters.query) {
            search_params.append('query', filters.query);
        }
        
        if (filters.category) {
            search_params.append('category', filters.category);
        }
        
        if (filters.min_price !== null) {
            search_params.append('min_price', filters.min_price.toString());
        }
        
        if (filters.max_price !== null) {
            search_params.append('max_price', filters.max_price.toString());
        }
        
        const api_url = `${API_BASE_URL}${SEARCH_ENDPOINT}?${search_params.toString()}`;
        const response = await fetch(api_url);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    }
    
    
    async fun_fetch_all_products() {
        const response = await fetch(`${API_BASE_URL}${PRODUCTS_ENDPOINT}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    }
    
    
    async fun_fetch_categories() {
        const response = await fetch(`${API_BASE_URL}${CATEGORIES_ENDPOINT}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    }
}


// Application Initialization
document.addEventListener('DOMContentLoaded', async () => {
    const search_view = new SearchView();
    const api_service = new ApiService();
    const search_controller = new SearchController(search_view, api_service);
    
    await search_controller.fun_initialize();
});