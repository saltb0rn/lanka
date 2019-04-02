<style scoped>

  .m-pannel {
      height: 100%;
      width: 100%;
  }

  .msg-area {
      height: 90%;
      overflow: hidden scroll;
      scroll-behavior: smooth;
  }

  .input-area {
      height: 10%;
      display: flex;
  }

  input {
      flex: 9
  }

  button {
      flex: 1
  }

  .msg-right {
      text-align: right;
      align-self: flex-end;
  }

  .msg-wrapper {
      display: flex;
      flex-direction: column;
      margin-bottom: 1em;
  }

  .msg {
      display: flex;
  }

  .msg-avator {
      display: flex;
      margin: 0 1em;
  }

  .msg-avator img {
      width: 50px;
      height: 50px;
      border-radius: 50%;
      background: black;
  }

  .msg-info {
      display: flex;
      flex-direction: column;
  }

  .msg-content {
      background: skyblue;
      padding: 1rem;
      border-radius: 4px;
      max-width: 50vw;
      word-wrap: break-all;
      white-space: pre-wrap;
  }

  .msg-content p {
      margin: 0;
  }
</style>

<template>
  <div class="m-pannel">
    <section class="msg-area">
      <div v-for="item in messageList"
           class="msg-wrapper">
        <div v-if="item.username == uname"
             class="msg"
             :class="{ 'msg-right' : uname == item.username}">
          <div class="msg-info">
            <div class="msg-sender">{{ item.username }}</div>
            <div class="msg-content" style="align-self: flex-end">
              <p>{{ item.message }}</p>
            </div>
          </div>
          <div class="msg-avator">
            <img />
          </div>
        </div>
        <div v-else class="msg">
          <div class="msg-avator">
            <img />
          </div>
          <div class="msg-info">
            <div class="msg-sender">{{ item.username }}</div>
            <div class="msg-content">
              <p>{{ item.message }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>
    <b-input-group prepend="Message" class="mt-3">
      <b-form-textarea v-model="msg"
                       rows="1"
                       />
      <b-input-group-append>
        <b-button variant="outline-succes" @click="sendMessage">Send Message</b-button>
      </b-input-group-append>
    </b-input-group>
  </div>
</template>

<script>
import BButton from 'bootstrap-vue/es/components/button/button';
import BInputGroup from 'bootstrap-vue/es/components/input-group/input-group';
import BFormTextarea from 'bootstrap-vue/es/components/form-textarea/form-textarea'
import Cookies from 'js-cookie';

export default {
    components: {
        BButton,
        BInputGroup,
        BFormTextarea
    },

    props: {
        wsserver: {
            type: String,
            required: true
        },
    },

    data: function() {
        return {
            msg: "",
            msgs: [],
            isSending: false
        };
    },

    methods: {
        sendMessage() {
            if(this.msg.length != 0) {
                this.isSending = true;
                this.ws.send(JSON.stringify({ body: this.msg }));

            }
        },

        scrollToBottom() {
            setTimeout((function() {
                this.msgArea.scrollTop = this.msgArea.scrollHeight;
            }).bind(this), 500);
        }
    },

    computed: {
        messageList: function() {
            return this.msgs;
        }
    },

    mounted() {
        this.msgArea = document.querySelector('.msg-area');

        if (!Cookies.get('uid')) {
            this.$router.push({name: 'login'});
            return;
        }

        let vm = this;
        this.ws = new WebSocket(vm.wsserver);
        this.ws.onopen = function() {
            vm.uname = Cookies.get('uname');
            Cookies.remove('uname');
            console.log('connected to chat server!');
        };
        this.ws.onmessage = function(evt) {
            let msg = JSON.parse(evt.data);

            if (msg.cached) {
                vm.msgs = msg.cached;
                vm.scrollToBottom();
                return;
            }
            vm.msgs.push(msg);
            if (vm.isSending) vm.scrollToBottom();
            vm.isSending = false;
            vm.msg = "";
        };
        this.ws.onclose = function() {
            Cookies.remove('uid');
            vm.$router.push({name: 'login'});
            console.log('you are leaving');
        };
    },
}
</script>
