console.log('hello from vue js scripts');
new Vue({
    delimiters: ['[[', ']]'],
    el: '#app_loading_naks_news',
    data() {
      return {
        info: null,
        post_title: null,
        post_sub_title: null,
        post_full_description: null,
        post_main_picture_url: null,
        post_published_date: null,
        counter: 0,
      };
    },
    mounted() {
      axios
        .get('/naks_api/posts/')
        .then(response => {
            this.info = response;
            // this.title = response.data.title;
            this.post_title = response.data.title;

        });
    },
    methods: {
        load_publication_content: function(event) {
            console.log('hi');
            if (event) {
                console.log(event.currentTarget.id);
                axios
                    .get(`/naks_api/posts/${event.currentTarget.id}`)
                    .then(response => {
                        this.post_title = response.data.title;
                        this.post_sub_title = response.data.subtitle;
                        this.post_full_description = response.data.full_description;
                        this.post_published_date = response.data.published_date;
                        if (response.data.main_picture == undefined || response.data.main_picture == null) {
                            this.post_main_picture_url = '/static/images/no_pict_icon.jpg'
                        } else {
                            this.post_main_picture_url = response.data.image_urls.medium;
                        }
                        this.counter += 1;
                        // console.log('response post title ', response.data.main_picture)
                    });
            }
        }
    }

  });