<style scoped>
  .login-pannel {
      margin: 1rem;
  }

  .submit-btn {
      display: flex;
  }

  button {
      margin: auto;
  }
</style>
<template>
  <div class="login-pannel">
    <b-form-group
      label-cols-sm="4"
      label-cols-lg="3"
      label="Identifier"
      label-for="identifier"
      >
      <b-form-input id="identifier" v-model="identifier" trim placeholder="Username or Email"/>
    </b-form-group>

    <b-form-group
      label-cols-sm="4"
      label-cols-lg="3"
      label="Password"
      label-for="password"
      >
      <b-form-input id="password" v-model="password" placeholder="Password" trim/>
    </b-form-group>

    <div class="submit-btn">
      <b-button variant="info" @click="login">Login</b-button>
      <b-button variant="info" @click="$router.push({name: 'register'})">Register</b-button>
    </div>
  </div>
</template>
<script>
import BButton from 'bootstrap-vue/es/components/button/button';
import BInputGroup from 'bootstrap-vue/es/components/input-group/input-group';
import BFormInput from 'bootstrap-vue/es/components/form-input/form-input';
import BFormGroup from 'bootstrap-vue/es/components/form-group/form-group'
import Cookies from 'js-cookie';

export default {

    props: {
        server: {
            type: String,
            required: true
        }
    },

    data: function() {
        return {
            identifier: null,
            password: null
        };
    },

    methods: {
        login() {
            // login if cookie is not set, otherwise redirect to chat page

            this.axios.post(`${this.server}/login`,
                            {
                                id: this.identifier,
                                password: this.password,
                            })
                .then(
                    (rsp) => {
                        if (rsp.data.result) {
                            this.$router.push({name: 'chat'});
                            Cookies.set('uname', rsp.data.username);

                        } else {
                            console.log('login failed');
                        }
                    }
                );
        }
    }


}
</script>
