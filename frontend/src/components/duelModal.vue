<template>
  <div id ="duelModal" class="modal">
    <div class="modal-content">You are have been challenged by {{ data }}. Accept?
      <span class="close" @click="$emit('close')">&times;</span>
      <button @click="acceptChallenge">Yes</button>
      <button @click="$emit('close')">No</button>
    </div>
  </div>
</template>

<script>
export default {
    props: ['data', 'connection'],
    methods: {
            acceptChallenge(){
              this.$emit('close')
              this.connection.emit('set up game', {'challengee_username': this.$store.state.username, 'challenger_username': this.data})
            }
        }
}
</script>

<style scoped>
/* The Modal (background) */
.modal {
  position: fixed; /* Stay in place */
  z-index: 1; /* Sit on top */
  left: 0;
  top: 0;
  width: 100%; /* Full width */
  height: 100%; /* Full height */
  overflow: auto; /* Enable scroll if needed */
  background-color: rgb(0,0,0); /* Fallback color */
  background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
}
/* Modal Content/Box */
.modal-content {
  text-align: center;
  background-color: #fefefe;
  margin: 15% auto; /* 15% from the top and centered */
  padding: 20px;
  border: 1px solid #888;
  width: 80%; /* Could be more or less, depending on screen size */
}
/* The Close Button */
.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}
</style>