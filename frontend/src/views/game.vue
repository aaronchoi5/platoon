<template>
    <div id="secure">
        <h1>Game View</h1>
    </div>
</template>

<script>
    export default {
        data(){
            return {
                cards: []
            }
        },
        created: function(){
            let connection = this.$store.state.connection

            connection.on('assign cards', (cards) => {
                this.cards = cards;
                console.log(this.cards)
            });
            connection.emit('get player cards', {'username': this.$store.state.username, 'gameId': this.$store.state.gameId})
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