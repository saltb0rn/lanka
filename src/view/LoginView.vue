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
    <login-pannel class="login-form" server="http://localhost:8000"></login-pannel>
  </div>
</div>
</template>
<script>
import LoginPannel from "../component/login.vue";

export default {
    components: {
        LoginPannel
    }
}
</script>
