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
                direction: '',
                counter: 0,
                reestrCenters: [],
                city_input: '',
                title_input: '',
                hidden: [],
                on_screen: [],
                row_ids: this.$refs,
            };
        },
        mounted() {
            // runs once
            this.iamhere();
            // console.log(this.$refs.direction.dataset.direction);
        },
        methods: {
            iamhere: function() {
                this.direction = this.$refs.direction.dataset.direction;
                let centers_updated_flag = this.$cookies.get("centers_storage_updated");
                if (localStorage.reestrCenters && centers_updated_flag) {
                        this.reestrCenters = JSON.parse(localStorage.reestrCenters);
                        console.log('taken from local storage', this.reestrCenters.length);
                } else {
                    this.load_reestr_centers();
                }
                this.reestrCenters = this.reestrCenters.filter(element => element.direction == this.direction)
                console.log('VUE is here', this);
            },
            load_reestr_centers: function() {
                axios
                    .get('/naks_api/centers/')
                    .then(response => {
                        localStorage.reestrCenters = JSON.stringify(response.data);
                        this.reestrCenters = JSON.stringify(response.data);
                        // this.reestrCenters = localStorage.reestrCenters;
                        console.log('saved to local storage', localStorage.reestrCenters.length);
                        this.$cookies.set("centers_storage_updated", "1", "1h");
                        console.log('cookies flag set up');
                    });
            },
            filter_by_city: function() {
                console.log('city_input', this.city_input);
            },
            onCityInput: function() {
                if (this.city_input.length > 1) {
                    this.hidden = this.reestrCenters.filter(element => !element.city.includes(this.city_input));

                    this.hide_filtered(this.hidden);
                    // for (var el of this.hidden) {
                    //         try {
                    //             let row_ = `${this.direction}_${el.id}`;
                    //                     let ref_ = this.$refs[row_];
                    //                     $(ref_).addClass('invisible');
                    //         } catch (error) {
                    //             console.log(error);
                    //         }
                    //     }
                        this.on_screen = this.reestrCenters.filter(element => !this.hidden.includes(element));
                        this.make_tables_unstriped();
                    } else {
                        console.log('else');

                    this.make_tables_unstriped();
                    this.show_if_hidden();
                }
            },
            onTitleInput: function() {
                if (this.title_input.length > 1) {
                    // this.hidden = this.reestrCenters.filter(element => !element.short_code.includes(this.title_input));
                    for (var i = 0; i < this.reestrCenters.length; i++) {
                        continue;
                    }
                    this.hide_filtered(this.hidden);
                } else {
                    console.log('else');

                this.make_tables_unstriped();
                this.show_if_hidden();
            }
                // console.log('title', this.title_input);
            },
            hide_filtered: function(arr) {
                for (var el of arr) {
                    try {
                        let row_ = `${this.direction}_${el.id}`;
                                let ref_ = this.$refs[row_];
                                $(ref_).addClass('invisible');
                    } catch (error) {
                        console.log(error);
                    }
                }
            },
            check: function() {
                console.log(this.hidden);
            },
            show_if_hidden: function() {
                for (var ref in this.$refs) {
                    var ref_ = this.$refs[ref];
                    if ($(ref_).hasClass("invisible")) {
                        $(ref_).removeClass('invisible');
                    }
                var tables = document.querySelectorAll('table');
                for (var t of tables) {
                    if ($(t).hasClass('table-hover')) {
                        $(t).addClass("table-striped");
                    }
                }
                }
            },
            make_tables_unstriped: function() {
                var tables = document.querySelectorAll('table');
                for (var table of tables) {
                    $(table).removeClass('table-striped');
                }
            }
        },
    });
}