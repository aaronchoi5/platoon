<template>
    <div id="secure">
        <h1>Game View</h1>
        <h2> wins: {{wins}} losses: {{losses}} draws: {{draws}}</h2>
        <button v-on:click="submitPiles()">Show me your moves!</button>
        <h3 v-if="authorized == false && submitted">Waiting for opponent to make a move</h3>
        <battleModal v-if="battleModalVisible" :connection=this.connection @close="battleModalVisible = false" :data="combatants" :authorized="authorized" @nturn="myFunction"/>
        <gameOverModal v-if="gameover" :result="result"/>
        <snackbar></snackbar>
            <div style="display: flex; justify-content: space-evenly">
                <div v-for="(opponentPile, opponentPIndex) in opponentPiles" style='display: inline-block' @click="assignOPile(opponentPIndex)">
                    <img class="imgCardHolder" v-bind:src= "require('../assets/cardframe.png')" width="70" height="120" style='margin-bottom: -7.75rem'/>
                    <img v-for= "index in opponentPiles[opponentPIndex]" v-bind:src= "require('../assets/tespaback.png')" width="70" height="120" style="display:block; margin-bottom: -6rem;"/>
                </div>
            </div>
            <div style="display: flex; justify-content: space-evenly; margin-top: 6rem;">
                <div v-for="(pile, pIndex) in piles" @click="assignCPile(pIndex)">
                    <CardHolder :id="getId(pIndex)" @carddrop="assign">
                        <Card v-for="(card,index) in pile" :card="card" :key="card.id" :draggable="true" :id="index" style="display: block"/>
                    </CardHolder>
                </div>
            </div>
        <Board id="board-2" @carddrop="assign">
              <Card v-for="(card,index) in cards" :card="card" :key="card.id" :draggable="true" :id="index"/>
        </Board>
    </div>
</template>

<script>
import Card from '@/components/Card.vue';
import CardHolder from '@/components/CardHolder.vue'
import Board from '@/components/Board.vue'
import battleModal from '@/components/battleModal.vue';
import snackbar from '@/components/snackbar.vue'
import gameOverModal from '@/components/gameOverModal.vue'
    export default {
        components : {
            battleModal,
            Board,
            Card,
            CardHolder,
            snackbar,
            gameOverModal
        },
        data(){
            return {
                authorized: false,
                connection: null,
                cards: [],
                piles: [[], [], [], [], []],
                opponentPiles: [0,0,0,0,0],
                chosenPile: -1,
                opponentPile: -1,
                battleModalVisible: false,
                combatants: [-1, -1],
                submitted: false,
                wins: 0,
                losses: 0,
                draws: 0,
                gameover: false,
                result: null 
            }
        },
        created: function(){
            this.connection = this.$store.state.connection
            this.connection.on('assign cards', (cards) => {
                for(var card in cards){
                    var temp = JSON.parse(cards[card]);
                    this.cards.push(temp);
                }
            });
            this.connection.emit('get player cards', {'username': this.$store.state.username, 'gameId': this.$store.state.gameId})

            this.connection.on('Waiting', () =>{
                //TODO: trigger some kind of waiting heading?
                console.log('waiting')
            });

            this.connection.on('Both Ready', (payload) =>{
                this.authorized = payload['authorized']
                let pileLengths = payload['piles']
                for(let i = 0; i < this.opponentPiles.length; i++){
                    this.opponentPiles.splice(i, 1, pileLengths[i])
                }
                this.submitted = true
            });

            this.connection.on('loss', (payload) =>{
                this.fightHandling(payload)
                this.losses += 1
            });

            this.connection.on('win', (payload) =>{
                this.fightHandling(payload)
                this.wins += 1
            });
            this.connection.on('draw', (payload) =>{
                this.fightHandling(payload)
                this.draws += 1
            });
            this.connection.on('win reset', (payload) =>{
                this.resetHandling(payload)
                this.wins += 1
            });

            this.connection.on('loss reset', (payload) =>{
                this.resetHandling(payload)
                this.losses += 1
            });
            
            this.connection.on('draw reset', (payload) =>{
                this.resetHandling(payload)
                this.draws += 1
            });
            this.connection.on('game over', (result) =>{
                this.gameover = true
                this.result = result
            });
        },
        methods:{
            assign: function(event){
                var pileId = event[2]
                let suit = event[0]
                let value = event[1]                    
                let card = {"value":parseInt(value), "suit":suit}
                this.deleteInstancesOfCard(card)

                if(pileId == "board-2"){
                    this.deleteCardFromPile(this.cards,JSON.stringify(card))
                    this.cards.push(card)

                }
                else{
                    this.piles[pileId].push(card)
                    this.deleteCardFromPile(this.cards,JSON.stringify(card))
                }
            },
            getId(index){
                return index
            },
            deleteInstancesOfCard(object){
                var jsonobj = JSON.stringify(object)
                for(let i = 0; i < this.piles.length; i++){
                    this.deleteCardFromPile(this.piles[i],jsonobj)
                }
            },
            deleteCardFromPile(pile, jsonobj){
                for(let i = 0; i < pile.length; i++){
                    if (JSON.stringify(pile[i]) == jsonobj){
                        pile.splice(i,1)
                    }
                }
            },
            submitPiles(){
                this.connection.emit('assign piles', {'username': this.$store.state.username, 'gameId': this.$store.state.gameId, 'piles': [this.piles[0], this.piles[1], this.piles[2], this.piles[3], this.piles[4]]})
            },
            assignOPile(pileId){
                this.opponentPile = pileId
                this.combatants[1] = this.opponentPile
                if (this.opponentPile != -1 && this.chosenPile != -1)
                {
                    this.battleModalVisible = true;
                }
            },
            assignCPile(pileId){
                this.chosenPile = pileId
                this.combatants[0] = this.chosenPile
                if (this.opponentPile != -1 && this.chosenPile != -1)
                {
                    this.battleModalVisible = true;
                }
            },
            myFunction() {
                // Get the snackbar DIV
                var x = document.getElementById("snackbar");

                // Add the "show" class to DIV
                x.className = "show";

                // After 3 seconds, remove the show class from DIV
                setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
                this.chosenPile = -1
                this.opponentPile = -1
            },
            fightHandling(payload){
                this.authorized = payload['authorized']
                let pilesA = payload['pilesA']
                for(let i = 0; i < this.piles.length; i++){
                    this.piles[i] = pilesA[i]
                }
                let pileLengths = payload['pilesB']
                for(let i = 0; i < this.opponentPiles.length; i++){
                    this.opponentPiles.splice(i, 1, pileLengths[i])
                }
                this.combatants[0] = this.combatants[1] = -1
                this.chosenPile = -1
                this.opponentPile = -1
            },
            resetHandling(payload){
                this.authorized = payload['authorized']
                let newCards = payload['newCards']
                for(var card in newCards){
                    var temp = JSON.parse(newCards[card]);
                    this.cards.push(temp);
                }
                for(let i = 0; i < this.opponentPiles.length; i++){
                    this.opponentPiles.splice(i, 1, 0)
                }
                for(let i = 0; i < this.piles.length; i++){
                    this.piles[i] = []
                }
                this.combatants[0] = this.combatants[1] = -1
                this.chosenPile = -1
                this.opponentPile = -1
                this.submitted = false
            }
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