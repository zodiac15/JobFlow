import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import JobDetailView from '../views/JobDetailView.vue'
import UserProfileView from '../views/UserProfileView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import SavedJobsView from '../views/SavedJobsView.vue'
import TrackerView from '../views/TrackerView.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView,
            meta: { title: 'JobFlow - Find Your Dream Tech Job' }
        },
        {
            path: '/job/:id',
            name: 'job-detail',
            component: JobDetailView,
            props: true,
            // Title handled in component
        },
        {
            path: '/profile',
            name: 'profile',
            component: UserProfileView,
            meta: { requiresAuth: true, title: 'My Profile - JobFlow' }
        },
        {
            path: '/login',
            name: 'login',
            component: LoginView,
            meta: { title: 'Login - JobFlow' }
        },
        {
            path: '/register',
            name: 'register',
            component: RegisterView,
            meta: { title: 'Register - JobFlow' }
        },
        {
            path: '/saved-jobs',
            name: 'saved-jobs',
            component: SavedJobsView,
            meta: { requiresAuth: true, title: 'Saved Jobs - JobFlow' }
        },
        {
            path: '/tracker',
            name: 'tracker',
            component: TrackerView,
            meta: { requiresAuth: true, title: 'Application Tracker - JobFlow' }
        },
        {
            path: '/admin',
            name: 'admin',
            component: () => import('../views/AdminDashboardView.vue'),
            meta: { requiresAuth: true, title: 'Admin Dashboard - JobFlow' }
        },
        {
            path: '/admin/jobs',
            name: 'admin-jobs',
            component: () => import('../views/AdminJobsView.vue'),
            meta: { requiresAuth: true, title: 'Manage Jobs - JobFlow' }
        },
        {
            path: '/admin/users',
            name: 'admin-users',
            component: () => import('../views/AdminUsersView.vue'),
            meta: { requiresAuth: true, title: 'Manage Users - JobFlow' }
        }
    ],
    scrollBehavior(to, from, savedPosition) {
        if (savedPosition) {
            return savedPosition
        } else {
            return { top: 0 }
        }
    }
})

router.beforeEach((to, from, next) => {
    // Auth Check
    const isAuthenticated = localStorage.getItem('user')
    if (to.meta.requiresAuth && !isAuthenticated) {
        return next('/login')
    }

    // SEO: Valid Title
    if (to.meta.title) {
        document.title = to.meta.title
    }

    next()
})

export default router
