console.log('hello from vue js scripts');

if (document.getElementById('app_loading_naks_news')) {
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
                post_has_main_picture: 0,
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
            load_publication_content: function (event) {
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
                                this.post_has_main_picture = 0
                            } else {
                                this.post_main_picture_url = response.data.image_urls.medium;
                                this.post_has_main_picture = 1
                            }
                            this.counter += 1;
                            // console.log('response post title ', response.data.main_picture)
                        });
                }
            }
        }

    });
}

if (document.getElementById('app_reestr_centers')) {
    // console.log('-->app reestr centers here');
    new Vue({
        delimiters: ['[[', ']]'],
        el: '#app_reestr_centers',
        data() {
            return {
                counter: 0,
                activeCenters: [],
                city_input: '',
                title_input: '',
                filtered: [],
                row_ids: this.$refs,
            };
        },
        mounted() {
            this.iamhere();
            let centers_updated_flag = this.$cookies.get("centers_storage_updated");
            if (localStorage.activeCenters && centers_updated_flag) {
                    this.activeCenters = JSON.parse(localStorage.activeCenters);
                    console.log('taken from local storage', this.activeCenters.length);
                // console.log('type of', typeof this.activeCenters);
            } else {
                this.load_active_centers();
            }
        },
        methods: {
            iamhere: function() {
                console.log('VUE is here', this);
                // console.log('REFS', this.$refs);
            },
            load_active_centers: function() {
                axios
                    .get('/naks_api/centers/')
                    .then(response => {
                        // console.log('RESPONSE', response);
                        // console.log('RESPONSE_type', typeof response);
                        // console.log('RESPONSE_data_type', typeof response.data);
                        // console.log('RESPONSE_data_first_element_type', typeof response.data[0]);
                        localStorage.activeCenters = JSON.stringify(response.data);
                        this.activeCenters = localStorage.activeCenters;
                        console.log('saved to local storage', localStorage.activeCenters.length);
                        this.$cookies.set("centers_storage_updated", "1", "1h");
                        console.log('cookies flag set up');
                    });
            },
            filter_by_city: function() {
                console.log('city_input', this.city_input);
            },
            onCityInput: function() {
                // console.log('city_input', this.city_input);
                if (this.city_input.length > 1) {
                    this.filtered = this.activeCenters.filter(element => !element.city.includes(this.city_input));
                    let counter = 0;
                    for (el of this.filtered) {
                        let row_ = `row_${el.id}`;
                        let row_to_hide = document.getElementById(row_);
                        try {
                            row_to_hide.style.display = 'none';
                        } catch (e) {
                            continue;
                        }
                        // console.log('el', this.filtered.length, el.city, row_to_hide, counter, el);
                        counter+=1;
                    }
                }
            },
            check: function() {
                // let filtered_rows = this.row_ids.filter(el => el.innerText.includes(this.city_input));
                // console.log('filtered rows', filtered_rows);
                // console.log('ROWS', this.row_ids)
                console.log(this.filtered);
            }
        },
    });
}