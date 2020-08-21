<template>
    <div :id="id" class="board" @dragover.prevent @drop.prevent="drop">
        <slot />
    </div>
</template>

<script>
export default {
    props:['id'],
    methods: {
        drop: function(e)  {
            const card_id = e.dataTransfer.getData('card_id');
            const card_suit = e.dataTransfer.getData('card_suit');
            const card_value = e.dataTransfer.getData('card_value');
            this.$emit('carddrop', [card_suit, card_value, this.id])

        }
    }
}
</script>

<style lang="scss" scoped>
    .board {
        background-color: green;
        margin-bottom: 10px;
        padding: 10px;
        position: absolute;
  		bottom: 10px;
  		height: 15%;
  		width: 100%;
        display: flex;
        justify-content: center;
        
      }
</style>