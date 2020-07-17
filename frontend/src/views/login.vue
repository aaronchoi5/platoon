<template>
    <div id="login">
        <h1>Login</h1>
        <input type="text" name="username" v-model="input.username" placeholder="Username" />
        <input type="password" name="password" v-model="input.password" placeholder="Password" />
        <button type="button" v-on:click="login()">Login</button>
    </div>
</template>

<script>
import axios from "axios";
import io from 'socket.io-client';

    export default {
        name: 'Login',
        data() {
            
            return {
                connection: null,
                input: {
                    username: "",
                    password: ""
                }
            }
        },
        methods: {
            login() {
                axios({ method: "POST", "url": "http://127.0.0.1:5000/login", "data": this.input, "headers": { "content-type": "application/json, Authorization" } }).then(result => {
                    if(result.status == 200){
                        this.$emit("authenticated", true);
                        this.$router.replace({ name: "secure" });
                    }
                    this.response = result.data;
                }, error => {
                    console.error(error);
                });
            }
        },
        created: function(){
            console.log("yooo");
            this.connection = io.connect('http://127.0.0.1:5000');
            this.connection.send('salutations')

            this.connection.on('connect', () => {
              console.log('Successfully connected!');
            });

        }
    }
</script>

<style scoped>
    #login {
        width: 500px;
        border: 1px solid #CCCCCC;
        background-color: #FFFFFF;
        margin: auto;
        margin-top: 200px;
        padding: 20px;
    }
</style>