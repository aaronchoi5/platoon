<template>
    <div id="secure">
        <h1>Game Lobby</h1>
        <p>
            List of users looking for games:
        </p>
        <myModal v-if="modalVisible" @close="modalVisible = false" :data="modalData"/>

        <option v-for="user in this.searchingUsers" :key="user.id" class="column is-one-third" @click="showModal(user)">{{user}}</option>
    </div>
</template>

<script>
import axios from "axios";
import io from 'socket.io-client';
import myModal from '@/views/myModal';
    export default {
        components:{
            myModal
        },
        name: 'Secure',
        data() {
            return {
                connection: null,
                games: [],
                searchingUsers : [],
                modalVisible: false,
                modalData: null
            };
        },
        
        mounted(){
            axios({ method: "GET", "url": "http://127.0.0.1:5000/lookingForGame", "data": this.input, "headers": { "content-type": "application/json, Authorization" } }).then(result => {
                        if(result.status == 200){
                            this.games = result.data
                            console.log(this.games)
                        }
                    }, error => {
                        console.error(error);
                    });
        },
        methods: {
            postGame(){
                axios({ method: "POST", "url": "http://127.0.0.1:5000/lookForGame", "data": this.input, "headers": { "content-type": "application/json, Authorization" } }).then(result => {
                    }, error => {
                        console.error(error);
                    });
            },
            showModal(user) {
                this.modalData = user
                this.modalVisible = true
            }
        },
        created: function(){
            console.log("connecting");
            this.connection = io.connect('http://127.0.0.1:5000');

            this.connection.on('connect', () => {
              console.log('Successfully connected!');
            });
 
             this.connection.on('looking for game users', (users) => {
                    console.log('star' + users.toString());
                    this.searchingUsers = users;
                    });
        }
    }
    
</script>

<style scoped>
    #secure {
        background-color: #FFFFFF;
        border: 1px solid #CCCCCC;
        padding: 20px;
        margin-top: 10px;
    }
</style>