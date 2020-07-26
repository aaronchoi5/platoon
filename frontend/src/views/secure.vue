<template>
    <div id="secure">
        <h1>Game Lobby</h1>
        <p>
            List of users looking for games:
        </p>
        <myModal v-if="modalVisible" :connection=this.connection @userChallenge="challengeUser" @close="modalVisible = false" :data="modalData"/>

        <option v-for="user in this.searchingUsers" :key="user.id" class="column is-one-third" @click="showModal(user)">{{user}}</option>
        <button @click="hostGame">Host Game</button>
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
        methods: {
            hostGame(){
                this.connection.emit('host game',this.$store.state.username )
            },
            showModal(user) {
                this.modalData = user
                this.modalVisible = true

            },
            challengeUser(data){
                this.connection.emit('user challenge', data)
            }
        },
        created: function(){
            this.connection = io.connect('http://127.0.0.1:5000');
            this.connection.emit('user session registration', this.$store.state.username);

            this.connection.on('connect', () => {
              console.log('Successfully connected!');
            });

             this.connection.on('looking for game users', (users) => {
                this.searchingUsers = users;
            });

            this.connection.emit('looking for game users')

            this.connection.on('challenge', (user) => {
                console.log(user)
                alert('You have been challenged by ' + user + '.')
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