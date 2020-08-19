import Vue from 'vue'
import VueRouter from 'vue-router'
import LoginComponent from "../views/login.vue"
import SecureComponent from "../views/secure.vue"
import RegisterComponent from "../views/register.vue"
import GameComponent from "../views/game.vue"

Vue.use(VueRouter)

export default new VueRouter({
    mode: 'history',
    routes: [
        {
            path: '/',
            redirect: {
                name: "login"
            }
        },
        {
            path: "/login",
            name: "login",
            component: LoginComponent
        },
        {
            path: "/secure",
            name: "secure",
            component: SecureComponent
        },
        {
            path: "/register",
            name: "register",
            component: RegisterComponent
        },
        {
            path: "/game",
            name: "game",
            component: GameComponent
        }
    ]
})