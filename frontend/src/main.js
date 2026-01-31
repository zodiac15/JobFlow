import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import { autoAnimatePlugin } from '@formkit/auto-animate/vue'
import { initCsrf } from './utils/api'

const app = createApp(App)

app.use(router)
    .use(autoAnimatePlugin)

// Initialize CSRF before mounting to ensure token exists
initCsrf().then(() => {
    app.mount('#app')
})
