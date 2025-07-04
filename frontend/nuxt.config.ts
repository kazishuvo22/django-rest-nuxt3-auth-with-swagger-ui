import {defineNuxtConfig} from 'nuxt/config';
import path from 'path';
import authRoutes from './modules/auth/routes';
import dashboardRoutes from './modules/dashboard/routes';
import homeRoutes from './modules/home/routes';
import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
    devtools: {enabled: true},
    modules: ['@pinia/nuxt'],
    alias: {
        '@auth': path.resolve(__dirname, 'modules/auth'),
        '@dashboard': path.resolve(__dirname, 'modules/dashboard'),
        '@home': path.resolve(__dirname, 'modules/home'),
    },
    runtimeConfig: {
        secretKey: process.env.SECRET_KEY, // Private
        public: {
            apiBase: process.env.NUXT_PUBLIC_API_BASE, // Public
        },
    },
    build: {
        transpile: ['jwt-decode'],
    },
    pages: true, // Enable filesystem routing
    hooks: {
        'pages:extend'(routes) {
            routes.push(
                ...authRoutes,
                ...dashboardRoutes,
                ...homeRoutes,
            );
        },
    },
    vite: {
        server: {
            watch: {
                usePolling: true,
                interval: 100, // Adjust the interval as needed
            },
        },
        plugins: [
            tailwindcss(),
        ],
    },
    app: {
        head: {
            link: [
                {
                    rel: 'stylesheet',
                    href: '/styles/global.css',
                },
            ],
        },
    },
    css: ['~/assets/css/main.css'],
    plugins: [
        '~/plugins/auth.js',
    ]
});
