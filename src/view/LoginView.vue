<style scoped>
.login-view {
    display: flex;
    height: 100vh;
    width: 100vw;
    background: linear-gradient(0deg, #0b4182 1%, #1e88e5 100%);
}

.login-form-wrapper {
    margin: auto;
    background-color: #fff;
    padding: 1em;
    border-radius: 4px;
}

.login-form {
    margin: auto;
}



</style>
<template>
<div class="login-view">
  <div class="login-form-wrapper">
    <login-pannel :server="server" class="login-form"></login-pannel>
  </div>
</div>
</template>
<script>
import LoginPannel from "../component/login.vue";

export default {
    props: {
        server: {
            type: String,
            required: true,
        }
    },

    components: {
        LoginPannel
    },
}
</script>
