<template>
    <div id="secure">
        <h1>Game Lobby</h1>
        <p>
            List of users looking for games:
        </p>
        <myModal v-if="modalVisible" :connection=this.connection @userChallenge="challengeUser" @close="modalVisible = false" :data="modalData"/>
        <duelModal v-if="showDuelModal" :connection=this.connection @close="showDuelModal = false" :data="challenger"/>

        <option v-for="user in this.searchingUsers" :key="user.id" class="column is-one-third" @click="showModal(user)">{{user}}</option>
        <button @click="hostGame">Host Game</button>
    </div>
</template>

<script>
import axios from "axios";
import io from 'socket.io-client';
import myModal from '@/components/myModal';
import duelModal from '@/components/duelModal';
    export default {
        components:{
            myModal,
            duelModal
        },
        name: 'Secure',
        data() {
            return {
                connection: null,
                searchingUsers : [],
                modalVisible: false,
                modalData: null,
                challenger: null,
                showDuelModal: false
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
            },
            setChallenger(challenger){
                this.challenger = challenger
            }
        },
        created: function(){
            this.connection = io.connect('http://127.0.0.1:5000');

            this.$store.commit('assignConnection', this.connection)

            this.connection.emit('user session registration', this.$store.state.username);

            this.connection.on('connect', () => {
              console.log('Successfully connected!');
            });

            this.connection.on('looking for game users', (users) => {
                this.searchingUsers = users;
            });

            this.connection.emit('looking for game users')

            this.connection.on('challenge', (user) => {
                this.setChallenger(user);
                this.showDuelModal = true;
            });

            this.connection.on('go to game view', (gameId) => {
                this.$store.commit('assignGameId', gameId)
                this.$router.replace({name: "game"})
            })
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