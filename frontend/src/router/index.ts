import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/streaming/StreamingView.vue')
    },
    {
      path: '/matches',
      name: 'matches',
      component: () => import('../views/matches/Matches.vue')
    },
    {
      path: '/management',
      name: 'management',
      component: () => import('../views/management/ManagementView.vue')
    },
    {
      path: '/management/:id',
      name: 'ManagementView',
      component: () => import('../views/management/PresenceReport.vue'),
      props: true
    },
    {
      path: '/recognize',
      name: 'recognize',
      component: () => import('../views/recognition/RecognitionView.vue')
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('../views/settings/SettingsView.vue')
    },
  ]
})

export default router
