<style scoped>
.chat-view {
    height: 100vh;
    width: 100vw;
    display: flex;
}

.chat-form-wrapper {
    margin: auto;
    height: 98vh;
    width: 98vw;
}

.chat-form {
    height: inherit;
    width: inherit;
}

</style>
<template>
<div class="chat-view">
  <div class="chat-form-wrapper">
    <message-pannel class="chat-form" :wsserver="server"></message-pannel>
  </div>
  </div>
</template>
<script>
import MessagePannel from "../component/messagePannel.vue";

export default {
    props: {
        server: {
            type: String,
            required: true,
        }
    },
    components: {
        MessagePannel
    }
}
</script>
