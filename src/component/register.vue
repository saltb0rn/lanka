<style scoped>
  .register-form {
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
<div class="register-form">

  <b-form-group
    label-cols-sm="4"
    label-cols-lg="3"
    label="Username"
    label-for="username"
    :state="usernameState"
    :invalidFeedback="feedbackForUsername"
    :validFeedback="feedbackForUsername"
    >

    <b-form-input id="username"
                  trim
                  placeholder="Username"
                  v-model="username"
                  @input="isUsernameExists"
                  />
  </b-form-group>

  <b-form-group
    label-cols-sm="4"
    label-cols-lg="3"
    label="Email"
    label-for="email"
    :state="emailState"
    :invalidFeedback="feedbackForEmail"
    :validFeedback="feedbackForEmail"
    >
    <b-form-input id="email"
                  trim
                  placeholder="Email"
                  v-model="email"
                  @input="isEmailRegistered"/>
  </b-form-group>

  <b-form-group
    label-cols-sm="4"
    label-cols-lg="3"
    label="Password"
    label-for="password"
    :state="passwordState"
    :invalidFeedback="feedbackForPassword"
    :validFeedback="feedbackForPassword"
    >

    <b-form-input id="password"
                  trim
                  v-model="password"
                  placeholder="Password"
                  @input="isPasswordRight" />

  </b-form-group>

  <b-form-group
    label-cols-sm="4"
    label-cols-lg="3"
    label="Password Comfirm"
    label-for="passwordComfirm"
    :state="passwordComfirmState"
    :invalidFeedback="feedbackForPasswordComfirm"
    :validFeedback="feedbackForPasswordComfirm"
    >

    <b-form-input id="passwordComfirm"
                  trim
                  placeholder="Password again"
                  v-model="passwordComfirm"
                  @input="isPasswordRight"/>
  </b-form-group>

  <div class="submit-btn">
    <b-button variant="info" @click="submit">Submit</b-button>
  </div>

</div>
</template>

<script>
import BButton from 'bootstrap-vue/es/components/button/button';
import BInputGroup from 'bootstrap-vue/es/components/input-group/input-group';
import BFormInput from 'bootstrap-vue/es/components/form-input/form-input';
import BFormGroup from 'bootstrap-vue/es/components/form-group/form-group'

function debounce(func, wait, immediate) {
    var delayed;
    return function() {
        var context = this, args = arguments;
        var callNow = immediate && !delayed;
        delayed && clearTimeout(delayed);
        delayed = setTimeout(
            () => (delayed = null) || (!immediate && func.apply(context, args)),
            wait);
        callNow && func.apply(context, args);
    };
}


function validateEmail(email) {
    var re = /^(?:[a-z0-9!#$%&amp;'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&amp;'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])$/;
    return re.test(email);
}

export default {
    props: {
        server: {
            type: String,
            required: true
        }
    },

    components: {
        BButton,
        BInputGroup,
        BFormInput
    },

    data: function() {
        return {
            username: null,
            email: null,
            password: null,
            passwordComfirm: null,
            isUsernameValid: null,
            isEmailValid: null,
            isPasswordValid: null,
            isPasswordComfirmValid: null,
            info: {}
        }
    },

    methods: {

        isUsernameExists: debounce(
            function() {
                // axios, return true or false, use debounced

                if (!this.username ||
                    this.username == "" ||
                    this.username.includes(' ')) {
                    this.isUsernameValid = false;
                    return;
                }
                this.axios.post(`${this.server}/preflight`, {
                    type: 'username',
                    value: this.username
                })
                    .then((rsp) => {
                        this.isUsernameValid = rsp.data.result;
                    })
            }, 500, false),

        isEmailRegistered: debounce(
            function() {
                if (!validateEmail(this.email) || this.email === "") {
                    this.isEmailValid = false;
                    return;
                }
                this.axios.post(`${this.server}/preflight`, {
                    type: 'email',
                    value: this.email
                })
                    .then((rsp) => {
                        this.isEmailValid = rsp.data.result;
                    })
            }, 500, false),

        isPasswordRight: debounce(
            function() {
                let res = (this.password && this.passwordComfirm) &&
                    (this.password == this.passwordComfirm) &&
                    (!this.password.includes(' '));
                this.isPasswordValid = res;
                this.isPasswordComfirmValid = res;
                return res;
            }, 500, false),

        submit: function() {
            if (!(this.usernameState && this.emailState && this.passwordState))
                return;
            this.axios.post(`${this.server}/register`,
                            {
                                username: this.username,
                                email: this.email,
                                password: this.password
                            })
                .then(
                    (rsp) => {
                        if (rsp.data.result) {
                            this.$router.push({name: 'chat'});
                        } else {
                            alert('Your registration is failed, please try again!');
                        }
                    })
        },
    },

    computed: {
        usernameState() {
            return this.isUsernameValid;
        },

        feedbackForUsername() {
            // if (this.isUsernameValid)
            // TODO: seems like the feedback function would not process the state other then the value of state is either true or false
            switch(this.isUsernameValid) {
            case true:
                return "It's OK"
            case false:
                return "Error: registered username or empty input";
            default:
                return "";
            }
        },

        emailState() {
            return this.isEmailValid;
        },

        feedbackForEmail() {
            switch(this.isEmailValid) {
            case true:
                return "It's OK"
            case false:
                return "Error: registered E-mail or invalid E-mail address";
            default:
                return "";
            }
        },

        passwordState() {
            return this.isPasswordValid;
        },

        feedbackForPassword() {
            return this.isPasswordValid ? "It's OK" : "NOT OK";
        },

        passwordComfirmState() {
            return this.isPasswordComfirmValid;
        },

        feedbackForPasswordComfirm() {
            return this.isPasswordComfirmValid ? "It's OK": "NOT OK";
        }

    }

}
</script>
