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
            } else {
                this.load_active_centers();
            }
        },
        methods: {
            iamhere: function() {
                console.log('VUE is here', this);
            },
            load_active_centers: function() {
                axios
                    .get('/naks_api/centers/')
                    .then(response => {
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
                console.log('city_input', this.city_input);
                if (this.city_input.length > 1) {
                    // let table = $('table.table-striped');
                    // table.removeClass('table-striped');
                    this.filtered = this.activeCenters.filter(element => !element.city.includes(this.city_input));
                    let counter = 0;
                    for (var el of this.filtered) {
                        if (el.direction == 'personal') {
                            let row_ = `personal_${el.id}`;
                            // let ref_ = el.temporary_suspend_date != '' ? this.$refs[row_] : continue;
                            if (el.temporary_suspend_date == null)
                                {
                                    let ref_ = this.$refs[row_]
                                    // console.log('row_personal', row_, 'ref', ref_, ref_ == undefined, el);
                                    // ref_.style.display = 'none';
                                    $(ref_).hide();
                                } else {
                                    continue;
                                }
                            // let row_to_hide = document.getElementById(row_);
                        }
                        // console.log('el', this.filtered.length, el.city, row_to_hide, counter, el);
                        counter+=1;
                    }
                    this.make_tables_striped();
                    console.log('this.filtered.length', this.filtered.length);
                } else {
                    this.make_tables_striped();
                    this.show_if_hidden();
                }
                // $("table").each(function(element) {
                //     var table = $(element);
                //     console.log('table', table);
                //     if (!table.hasClass('table-striped')) {
                //         table.addClass('table-striped');
                //     }
                // });
            },
            check: function() {
                // let filtered_rows = this.row_ids.filter(el => el.innerText.includes(this.city_input));
                // console.log('filtered rows', filtered_rows);
                // console.log('ROWS', this.row_ids)
                console.log(this.filtered);
            },
            show_if_hidden: function() {
                // console.log(this.$refs, typeof this.$refs);
                for (var ref in this.$refs) {
                    var ref_ = this.$refs[ref];
                    if ($(ref_).is(":hidden")) {
                        $(ref_).show();
                    }
                var tables = document.querySelectorAll('table');
                for (var t of tables) {
                    if ($(t).hasClass('table-hover')) {
                        $(t).addClass("table-striped");
                    }
                }
                // $('table').each(function(element){
                //     $(element).addClass('table-striped');
                // });


                    // if (ref_.style.display == 'none') {
                    //     ref_.style.display = 'table';
                    // }
                    // console.log(ref_);
                }
            },
            make_tables_striped: function() {
                var tables = document.querySelectorAll('table');
                for (var table of tables) {
                    $(table).removeClass('table-striped');
                }

            }
        },
    });
}