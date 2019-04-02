<style scoped>
.register-view {
    display: flex;
    height: 100vh;
    width: 100vw;
    background: linear-gradient(0deg, #0b4182 1%, #1e88e5 100%);
}

.register-form-wrapper {
    margin: auto;
    background-color: #fff;
    border-radius: 4px;
}

@media screen and (max-width: 360px) {
    .register-form-wrapper {
        width: 98%;
    }
}

.register-form {
    padding: 1em;
    margin: auto;
}
</style>

<template>
<div class="register-view">
  <div class="register-form-wrapper">
    <register-pannel class="register-pannel" :server="server"></register-pannel>
  </div>
</div>
</template>

<script>
import RegisterPannel from "../component/register.vue";

export default {

    props:  {
        server: {
            type: String,
            required: true
        }
    },

    components: {
        RegisterPannel
    }
}
</script>
