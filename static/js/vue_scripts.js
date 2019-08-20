console.log('hello from vue js scripts');
new Vue({
    delimiters: ['[[', ']]'],
    el: '#app_loading_naks_news',
    data() {
      return {
        info: null,
        post_title: null,
        post_full_description: null,
        post_main_picture_url: null,
        counter: 0,
      };
    },
    mounted() {
      axios
        .get('/naks_api/posts/201')
        .then(response => {
            this.info = response;
            // this.title = response.data.title;
            this.post_title = response.data.title;

        });
    },
    methods: {
        greet: function(event) {
            console.log('hi');
            if (event) {
                console.log(event.currentTarget.id);
                axios
                    .get(`/naks_api/posts/${event.currentTarget.id}`)
                    .then(response => {
                        this.post_title = response.data.title;
                        this.post_full_description = response.data.full_description;
                        this.post_main_picture_url = response.data.main_picture;
                        this.counter += 1;
                        console.log('response post title ', response.data.title)
                    });
            }
        }
    }

  });