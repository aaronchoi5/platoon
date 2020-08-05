<template>
    <div id="secure">
        <h1>Game View</h1>
        <button v-on:click="submitPiles()">Show me your moves!</button>
            <div style="display: flex; justify-content: space-evenly">
                <CardHolder id="c1" @carddrop="assign">
                    <Card v-for="(card,index) in pile1" :card="card" :key="card.id" :draggable="true" :id="index" style="display: block"/>
                </CardHolder>
                <CardHolder id="c2" @carddrop="assign">
                    <Card v-for="(card,index) in pile2" :card="card" :key="card.id" :draggable="true" :id="index" style="display: block"/>
                </CardHolder>
                <CardHolder id="c3" @carddrop="assign">
                    <Card v-for="(card,index) in pile3" :card="card" :key="card.id" :draggable="true" :id="index" style="display: block"/>
                </CardHolder>
                <CardHolder id="c4" @carddrop="assign">
                    <Card v-for="(card,index) in pile4" :card="card" :key="card.id" :draggable="true" :id="index" style="display: block"/>
                </CardHolder>
                <CardHolder id="c5" @carddrop="assign">
                    <Card v-for="(card,index) in pile5" :card="card" :key="card.id" :draggable="true" :id="index" style="display: block"/>
                </CardHolder>
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
import draggable from 'vuedraggable';
    export default {
        components : {
            Board,
            Card,
            CardHolder,
            draggable
        },
        data(){
            return {
                connection: null,
                cards: [],
                pile1: [],
                pile2: [],
                pile3: [],
                pile4: [],
                pile5: []
            }
        },
        created: function(){
            let connection = this.$store.state.connection
            this.connection = connection
            connection.on('assign cards', (cards) => {
                for(var card in cards){
                    var temp = JSON.parse(cards[card]);
                    this.cards.push(temp);
                }
            });
            connection.emit('get player cards', {'username': this.$store.state.username, 'gameId': this.$store.state.gameId})
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
                        this.pile1.push(card)
                        this.deleteCardFromPile(this.cards,JSON.stringify(card))
                        break;
                    case "c2":
                        this.pile2.push(card)
                        this.deleteCardFromPile(this.cards,JSON.stringify(card))
                        break;
                    case "c3":
                        this.pile3.push(card)
                        this.deleteCardFromPile(this.cards,JSON.stringify(card))
                        break;
                    case "c4":
                        this.pile4.push(card)
                        this.deleteCardFromPile(this.cards,JSON.stringify(card))
                        break;
                    case "c5":
                        this.pile5.push(card)
                        this.deleteCardFromPile(this.cards,JSON.stringify(card))
                        break;
                    case "board-2":
                        this.cards.push(card)
                        break;
                }

            },
            deleteInstancesOfCard(object){
                var jsonobj = JSON.stringify(object)
                this.deleteCardFromPile(this.pile1,jsonobj)
                this.deleteCardFromPile(this.pile2,jsonobj)
                this.deleteCardFromPile(this.pile3,jsonobj)
                this.deleteCardFromPile(this.pile4,jsonobj)
                this.deleteCardFromPile(this.pile5,jsonobj)
            },
            deleteCardFromPile(pile, jsonobj){
                for(let i = 0; i < pile.length; i++){
                    if (JSON.stringify(pile[i]) == jsonobj){
                        pile.splice(i,1)
                    }
                }
            },
            submitPiles(){
                this.connection.emit('assign piles', {'username': this.$store.state.username, 'gameId': this.$store.state.gameId, 'piles': [this.pile1, this.pile2, this.pile3, this.pile4, this.pile5]})
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