<template>
  <div>
    <a :id="id" class="cardHolder" @dragover.prevent @drop.prevent="drop" href="#" >
        <img class="imgCardHolder" v-bind:src= "require('../assets/cardframe.png')" width="70" height="120"/>
          <slot />
    </a>
  </div>
</template>

<script>
export default {
    data(){
      return{
        showTestModal: false
      }
    },
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
    .cardHolder {
        background-color: #eee;
        margin-top: 5rem;
        margin-bottom: 10px;
        display: inline-block;
        width: 80px;
        height: 120px;
      }
    .imgCardHolder{
      margin-bottom:-8rem;
    }
    .cardHolder:focus{
      outline: 5px dashed red;
    }
</style>