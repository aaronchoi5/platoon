<template>

      <img v-bind:src= "require('../assets/' + card.value + card.suit + '.png')" width="70" height="120" class="card-content" :draggable="draggable" :id="id" @dragstart="dragStart" @dragover.stop :suit=card.suit :value=card.value @dragover.prevent @drop.prevent="drop"/>

</template>
<script>
export default {
  props: [
    'card',
    'id',
    'draggable'
  ],
  methods:{
    dragStart: e=> {
      const target = e.target;
      e.dataTransfer.setData('card_id', target.id);
      e.dataTransfer.setData('card_suit', target.getAttribute("suit"))
      e.dataTransfer.setData('card_value', target.getAttribute("value"))           
    },
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
  .card-content {
    padding-top: 50px;
    position: relative;
    top: 0;
    padding: 10px;
    height: 120px;
    width: 70px;
    display: inline-block;
    margin-bottom: -7.5rem;

  }
</style>