export default {
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'frontend',
    htmlAttrs: {
      lang: 'en'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
      { name: 'format-detection', content: 'telephone=no' }
    ],
    link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }]
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/bootstrap
    'bootstrap-vue/nuxt',
    '@nuxtjs/axios',
    '@nuxtjs/auth-next'
  ],

  // Axios module configuration
  axios: {
    baseURL: process.env.HEROKU_BACKEND_API_URL,
    browserBaseURL: process.env.HEROKU_BACKEND_API_URL
  },

  // Auth module configuration: https://auth.nuxtjs.org/guide/setup
  auth: {
    strategies: {
      local: {
        scheme: 'refresh',
        localStorage: {
          prefix: 'auth.'
        },
        token: {
          prefix: 'access_token',
          property: 'access_token',
          maxAge: 1800,
          // global: true
          type: 'Bearer'
        },
        refreshToken: {
          prefix: 'refresh_token',
          property: 'refresh_token',
          data: 'refresh_token',
          maxAge: 60 * 60 * 24 * 30
        },
        user: {
          property: 'user',
          autoFetch: true
        },
        endpoints: {
          login: { url: '/login', method: 'post' },
          refresh: { url: '/token_refresh', method: 'post' },
          user: { url: '/me', method: 'get' },
          logout: false // { url: '/logout', method: 'post' }
        }
        // autoLogout: false
      }
    }
  },
  // Install the `IconsPlugin` plugin (in addition to `BootstrapVue` plugin)
  bootstrapVue: {
    icons: true
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {},

  // Nuxt/auth settings for middleware set globally
  router: {
    middleware: ['auth']
  },

  // Nuxt parameter for deployment
  target: 'server'
};
