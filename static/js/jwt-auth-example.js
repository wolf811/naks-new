const store = new Vuex.Store({
    state: {
        authUser: {},
        isAuthenticated: false,
        jwt: localStorage.getItem('token'),
      endpoints: {
        // obtainJWT: '/api-token-auth/',
        // refreshJWT: '/api-token-refresh/',
        // verifyJWT:  '/api-token-verify/'
        obtainJWT: '/api-token-auth/',
        refreshJWT: '/api-token-refresh/',
        baseUrl: '/'
      }
    },
    mutations: {
        setAuthUser(state, {
          authUser,
          isAuthenticated
        }) {
          Vue.set(state, 'authUser', authUser)
          Vue.set(state, 'isAuthenticated', isAuthenticated)
        },
        updateToken(state, newToken) {
          // TODO: For security purposes, take localStorage out of the project.
          localStorage.setItem('token', newToken);
          state.jwt = newToken;
        },
        removeToken(state) {
          // TODO: For security purposes, take localStorage out of the project.
          localStorage.removeItem('token');
          state.jwt = null;
        }
      }
})


if ($('#auth_app').length > 0) {
    var vm_auth = new Vue({
        delimiters: ['[[', ']]'],
        el: '#auth_app',
        data() {
            return {
                title: 'auth_app',
                logged_in: true,
                username: '',
                password: '',
                endpoints: {
                    // path('api-token-auth/', obtain_jwt_token),
                    // path('api-token-refresh/', refresh_jwt_token),
                    // path('api-token-verify/', verify_jwt_token),
                    obtainJWT: '/api-token-auth/',
                    refreshJWT: '/api-token-refresh/',
                    verifyJWT:  '/api-token-verify/'
                }
            }
        },
        beforeMount() {
            this.jwt = localStorage.getItem('jwtToken')
            // if ((this.jwt).length == 0) {
            //     localStorage.setItem('token', newToken)
            // }
        },
        methods: {
            authenticate: function() {
                const payload = {
                    email: this.username,
                    password: this.password
                }
                const base = {
                    baseURL: this.$store.state.endpoints.baseUrl,
                    headers: {
                    // Set your Authorization to 'JWT', not Bearer!!!
                      Authorization: `JWT ${this.$store.state.jwt}`,
                      'Content-Type': 'application/json'
                    },
                    xhrFields: {
                        withCredentials: true
                    }
                }
                axios
                    .post(this.$store.state.endpoints.obtainJWT, payload)
                    .then(response => {
                        // localStorage.setItem('token', newToken);
                        this.$store.commit('updateToken', response.data.token)
                        // const newToken = response.data.token;
                        localStorage.setItem('token', newToken);
                    })
                    .finally()
            },
            logout_current_user: function() {
                // var data = {
                //     logout_current_user: true,
                // }
                let formData = new FormData();
                formData.append('logout_current_user', true);
                axios
                .post('/users/logout/', formData)
                .then(response => {
                    console.log('response', response.data);
                    this.logged_in = false;
                })
                .finally(() => {
                    // this.$cookies.set("sro_members_updated", "1", "1h");
                    console.log('finally logout callback');
                })
            }
        }
    });
}