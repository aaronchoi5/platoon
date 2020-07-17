<template>
    <div>{{ data }}
      <button @click="$emit('close')">Cancel</button>
    </div>
</template>

<script>
export default {
    props: ['data']
}
</script>
