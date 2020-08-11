<template>
    <div id="secure">
        <h1>Game View</h1>
        <h2> wins: {{wins}} losses: {{losses}} draws: {{draws}}</h2>
        <button v-on:click="submitPiles()">Show me your moves!</button>
        <button v-on:click="test()">Test</button>
        <battleModal v-if="battleModalVisible" :connection=this.connection @close="battleModalVisible = false" :data="combatants"/>
            <div style="display: flex; justify-content: space-evenly">
                <div id="o1" style='display: inline-block' @click="assignOPile(0)">
                    <img v-for= "index in oPile0" v-bind:src= "require('../assets/tespaback.png')" width="70" height="120" style="display:block; margin-bottom: -6rem;"/>
                </div>
                <div id="o2" style='display: inline-block' @click="assignOPile(1)">
                    <img v-for= "index in oPile1" v-bind:src= "require('../assets/tespaback.png')" width="70" height="120" style="display:block; margin-bottom: -6rem;"/>
                </div>
                <div id="o3" style='display: inline-block' @click="assignOPile(2)">
                    <img v-for= "index in oPile2" v-bind:src= "require('../assets/tespaback.png')" width="70" height="120" style="display:block; margin-bottom: -6rem;"/>
                </div>
                <div id="o4" style='display: inline-block' @click="assignOPile(3)">
                    <img v-for= "index in oPile3" v-bind:src= "require('../assets/tespaback.png')" width="70" height="120" style="display:block; margin-bottom: -6rem;"/>
                </div>
                <div id="o5" style='display: inline-block' @click="assignOPile(4)">
                    <img v-for= "index in oPile4" v-bind:src= "require('../assets/tespaback.png')" width="70" height="120" style="display:block; margin-bottom: -6rem;"/>
                </div>
            </div>
            <div style="display: flex; justify-content: space-evenly; margin-top: 6rem;">
                <div  @click="assignCPile(0)">
                    <CardHolder id="c1" @carddrop="assign">
                        <Card v-for="(card,index) in pile0" :card="card" :key="card.id" :draggable="true" :id="index" style="display: block"/>
                    </CardHolder>
                </div>
                <div  @click="assignCPile(1)">
                    <CardHolder id="c2" @carddrop="assign" @click="assignCPile(1)">
                        <Card v-for="(card,index) in pile1" :card="card" :key="card.id" :draggable="true" :id="index" style="display: block"/>
                    </CardHolder>
                </div>
                <div  @click="assignCPile(2)">
                    <CardHolder id="c3" @carddrop="assign" @click="assignCPile(2)">
                        <Card v-for="(card,index) in pile2" :card="card" :key="card.id" :draggable="true" :id="index" style="display: block"/>
                    </CardHolder>
                </div>
                <div  @click="assignCPile(3)">
                    <CardHolder id="c4" @carddrop="assign" @click="assignCPile(3)">
                        <Card v-for="(card,index) in pile3" :card="card" :key="card.id" :draggable="true" :id="index" style="display: block"/>
                    </CardHolder>
                </div>
                <div  @click="assignCPile(4)">
                    <CardHolder id="c5" @carddrop="assign" @click="assignCPile(4)">
                        <Card v-for="(card,index) in pile4" :card="card" :key="card.id" :draggable="true" :id="index" style="display: block"/>
                    </CardHolder>
                </div>
            </div>
        <Board id="board-2" @carddrop="assign">
              <Card v-for="(card,index) in cards" :card="card" :key="card.id" :draggable="true" :id="index"/>
        </Board>
    </div>
</template>

<script>
import Card from '../components/Card.vue';
import CardHolder from '../components/CardHolder.vue'
import Board from '../components/Board.vue'
import battleModal from '@/views/battleModal.vue';
import draggable from 'vuedraggable';
    export default {
        components : {
            battleModal,
            Board,
            Card,
            CardHolder,
            draggable
        },
        data(){
            return {
                authorized: null,
                connection: null,
                cards: [],
                pile0: [],
                pile1: [],
                pile2: [],
                pile3: [],
                pile4: [],
                oPile0: 0,
                oPile1: 0,
                oPile2: 0,
                oPile3: 0,
                oPile4: 0,
                chosenPile: -1,
                opponentPile: -1,
                battleModalVisible: false,
                combatants: [-1, -1],
                wins: 0,
                losses: 0,
                draws: 0
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
                console.log('waiting')
            });

            this.connection.on('Both Ready', (payload) =>{
                this.authorized = payload['authorized']
                let pileLengths = payload['piles']
                this.oPile0 = pileLengths[0]
                this.oPile1 = pileLengths[1]
                this.oPile2 = pileLengths[2]
                this.oPile3 = pileLengths[3]
                this.oPile4 = pileLengths[4]
            });
            this.connection.on('loss', (payload) =>{
                let pilesA = payload['pilesA']
                this.pile0 = pilesA[0]
                this.pile1 = pilesA[1]
                this.pile2 = pilesA[2]
                this.pile3 = pilesA[3]
                this.pile4 = pilesA[4]

                let pileLengths = payload['pilesB']
                this.oPile0 = pileLengths[0]
                this.oPile1 = pileLengths[1]
                this.oPile2 = pileLengths[2]
                this.oPile3 = pileLengths[3]
                this.oPile4 = pileLengths[4]
                this.combatants[0] = this.combatants[1] = -1
                this.chosenPile = -1
                this.opponentPile = -1
                this.losses += 1
            });
            this.connection.on('win', (payload) =>{
                let pilesA = payload['pilesA']
                this.pile0 = pilesA[0]
                this.pile1 = pilesA[1]
                this.pile2 = pilesA[2]
                this.pile3 = pilesA[3]
                this.pile4 = pilesA[4]

                let pileLengths = payload['pilesB']
                this.oPile0 = pileLengths[0]
                this.oPile1 = pileLengths[1]
                this.oPile2 = pileLengths[2]
                this.oPile3 = pileLengths[3]
                this.oPile4 = pileLengths[4]
                this.combatants[0] = this.combatants[1] = -1
                this.chosenPile = -1
                this.opponentPile = -1
                this.wins += 1
            });
            this.connection.on('win reset', (newCards) =>{
                for(var card in newCards){
                    var temp = JSON.parse(newCards[card]);
                    this.cards.push(temp);
                }
                this.oPile0 = 0
                this.oPile1 = 0
                this.oPile2 = 0
                this.oPile3 = 0
                this.oPile4 = 0
                this.pile0 = []
                this.pile1 = []
                this.pile2 = []
                this.pile3 = []
                this.pile4 = []

                this.combatants[0] = this.combatants[1] = -1
                this.chosenPile = -1
                this.opponentPile = -1
                this.wins += 1
            });
            this.connection.on('loss reset', (newCards) =>{
                for(var card in newCards){
                    var temp = JSON.parse(newCards[card]);
                    this.cards.push(temp);
                }

                this.oPile0 = 0
                this.oPile1 = 0
                this.oPile2 = 0
                this.oPile3 = 0
                this.oPile4 = 0
                this.pile0 = []
                this.pile1 = []
                this.pile2 = []
                this.pile3 = []
                this.pile4 = []

                this.combatants[0] = this.combatants[1] = -1
                this.chosenPile = -1
                this.opponentPile = -1
                this.losses += 1
            });
            this.connection.on('game over', (payload) =>{
                console.log('waiting')
            });
            this.connection.on('draw', (payload) =>{
                let pilesA = payload['pilesA']
                this.pile0 = pilesA[0]
                this.pile1 = pilesA[1]
                this.pile2 = pilesA[2]
                this.pile3 = pilesA[3]
                this.pile4 = pilesA[4]

                let pileLengths = payload['pilesB']
                this.oPile0 = pileLengths[0]
                this.oPile1 = pileLengths[1]
                this.oPile2 = pileLengths[2]
                this.oPile3 = pileLengths[3]
                this.oPile4 = pileLengths[4]
                this.combatants[0] = this.combatants[1] = -1
                this.chosenPile = -1
                this.opponentPile = -1
                this.draw += 1
            });
        },
        methods:{
            assign: function(event){
                var pileId = event[2]
                let suit = event[0]
                let value = event[1]                    
                let card = {"value":parseInt(value), "suit":suit}
                this.deleteInstancesOfCard(card)

                switch(pileId){
                    case "c1":
                        this.pile0.push(card)
                        this.deleteCardFromPile(this.cards,JSON.stringify(card))
                        break;
                    case "c2":
                        this.pile1.push(card)
                        this.deleteCardFromPile(this.cards,JSON.stringify(card))
                        break;
                    case "c3":
                        this.pile2.push(card)
                        this.deleteCardFromPile(this.cards,JSON.stringify(card))
                        break;
                    case "c4":
                        this.pile3.push(card)
                        this.deleteCardFromPile(this.cards,JSON.stringify(card))
                        break;
                    case "c5":
                        this.pile4.push(card)
                        this.deleteCardFromPile(this.cards,JSON.stringify(card))
                        break;
                    case "board-2":
                        this.cards.push(card)
                        break;
                }
            },
            deleteInstancesOfCard(object){
                var jsonobj = JSON.stringify(object)
                this.deleteCardFromPile(this.pile0,jsonobj)
                this.deleteCardFromPile(this.pile1,jsonobj)
                this.deleteCardFromPile(this.pile2,jsonobj)
                this.deleteCardFromPile(this.pile3,jsonobj)
                this.deleteCardFromPile(this.pile4,jsonobj)
            },
            deleteCardFromPile(pile, jsonobj){
                for(let i = 0; i < pile.length; i++){
                    if (JSON.stringify(pile[i]) == jsonobj){
                        pile.splice(i,1)
                    }
                }
            },
            submitPiles(){
                this.connection.emit('assign piles', {'username': this.$store.state.username, 'gameId': this.$store.state.gameId, 'piles': [this.pile0, this.pile1, this.pile2, this.pile3, this.pile4]})
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
            test(){
                this.connection.emit('test', {'username': this.$store.state.username, 'gameId': this.$store.state.gameId})
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