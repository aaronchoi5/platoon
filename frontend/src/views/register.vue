<template>
    <div id="login">
        <h1>Register</h1>
        <input type="text" name="username" v-model="input.username" placeholder="Username" />
        <input type="password" name="password" v-model="input.password" placeholder="Password" />
        <button type="button" v-on:click="register()">Register</button>
    </div>
</template>

<script>
import axios from "axios";
export default {
        name: 'Register',
        data() {
            return {
                input: {
                    username: "",
                    password: ""
                }
            }
        },
        methods: {
            register() {
                axios({ method: "POST", "url": "http://74.215.43.246:5000/register", "data": this.input, "headers": { "content-type": "application/json, Authorization" } }).then(result => {
                    if(result.status == 200){
                        this.$router.replace({ name: "login" });
                    }
                    this.response = result.data;
                }, error => {
                    console.error(error);
                });
            }
        }

    }
</script>