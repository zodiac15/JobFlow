import { ref } from 'vue'

// API Base URL from environment variable or fallback to localhost
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'

const csrfToken = ref('')

/**
 * Resolve a URL to its full form
 * @param {string} url - Relative or absolute URL
 * @returns {string} - Full URL
 */
export const resolveUrl = (url) => {
    // If URL is already absolute (starts with http:// or https://), return as-is
    if (url.startsWith('http://') || url.startsWith('https://')) {
        return url
    }
    // Otherwise, prepend the API base URL
    // Remove leading slash from url if present to avoid double slashes
    const path = url.startsWith('/') ? url : `/${url}`
    return `${API_BASE_URL}${path}`
}

export const initCsrf = async () => {
    try {
        const response = await fetch(resolveUrl('/api/csrf-token'), { credentials: 'include' })
        const data = await response.json()
        csrfToken.value = data.csrf_token
    } catch (e) {
        console.error("Failed to fetch CSRF token", e)
    }
}

export const fetchWithAuth = async (url, options = {}) => {
    // Resolve URL to full form
    const fullUrl = resolveUrl(url)

    // Ensure credentials are sent
    options.credentials = 'include'

    // Default headers
    options.headers = {
        ...options.headers,
    }

    // Add CSRF Token for state-changing methods
    if (['POST', 'PUT', 'DELETE', 'PATCH'].includes(options.method?.toUpperCase())) {
        options.headers['X-CSRFToken'] = csrfToken.value
    }

    return fetch(fullUrl, options)
}

// Export API_BASE_URL for direct use if needed
export { API_BASE_URL }
