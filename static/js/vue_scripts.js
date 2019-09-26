console.log('hello from vue js scripts');

// function arrayRemove(arr, value) {
//     return arr.filter( function(el) { return el != value; })
// }

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
                city_input_length: 0,
                title_input: '',
                title_input_length: 0,
                special_gp: false,
                special_tn: false,
                on_screen: [],
                row_ids: this.$refs,
                parametersAccumulator: [],
            };
        },
        mounted() {
            this.iamhere();
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
            onCityInput_depricated: function() {
                if (this.city_input.length > 1) {
                    this.hidden = this.reestrCenters.filter(element => !element.city.includes(this.city_input));

                    this.hide_filtered(this.hidden);
                        this.on_screen = this.reestrCenters.filter(element => !this.hidden.includes(element));
                        this.make_tables_unstriped();
                    } else {
                        console.log('else');

                    this.make_tables_unstriped();
                    this.show_if_hidden();
                }
            },
            onCityInput: function() {
                this.filterByInput({'parameter': 'city', 'value': this.city_input});
                    if (this.city_input.length < this.city_input_length) {
                        this.city_input_length = this.city_input.length;
                        this.show_hidden_centers(this.on_screen);
                    } else {
                        this.city_input_length = this.city_input.length;
                        this.show_filtered(this.on_screen);
                    }
                    this.make_tables_unstriped();
            },
            onTitleInput: function() {
                this.filterByInput({'parameter': 'short_code', 'value': this.title_input});
                if (this.title_input.length < this.title_input_length) {
                        this.title_input_length = this.title_input.length;
                        this.show_hidden_centers();
                    } else {
                        this.title_input_length = this.title_input.length;
                        this.show_filtered(this.on_screen);
                    }
                    this.make_tables_unstriped();
            },
            filterByInput: function(input_data) {
                if (!this.parametersAccumulator.includes(input_data)) {
                    for(var element of this.parametersAccumulator) {
                        if (element.parameter == input_data.parameter) {
                            this.parametersAccumulator.splice(this.parametersAccumulator.indexOf(element), 1);
                        }
                    }
                    this.parametersAccumulator.push(input_data);
                }
                var result_array = [];

                for (var element of this.reestrCenters) {
                    var passing = true;
                    for (var param of this.parametersAccumulator) {
                        // console.log(param.parameter, param.value, element, element[param.parameter].includes(param.value));
                        if (!element[param.parameter].includes(param.value)) {
                            passing = false;
                            break;
                        }
                    }
                    if (passing) {
                        result_array.push(element);
                    }
                }
                console.log('RESULT_ARRAY', result_array);
                this.on_screen = result_array;

            },
            show_filtered: function(arr) {
                console.log('to show', arr);
                    for (var el of this.reestrCenters) {
                        if (arr.includes(el)) {
                            continue;
                        } else {
                            let row_ = `${this.direction}_${el.id}`;
                            let ref_ = this.$refs[row_];
                            $(ref_).addClass('invisible');
                        }
                    }
            },
            check: function() {
                console.log(this.hidden);
            },
            show_hidden_centers: function() {
                for (var el of this.on_screen) {
                    var row_ = `${this.direction}_${el.id}`;
                    var ref_ = this.$refs[row_];
                    if ($(ref_).hasClass('invisible')) {
                        $(ref_).removeClass('invisible')
                    }
                }
            },
            reset_filters: function() {
                if (this.city_input.length != 0 || this.title_input.length !=0) {
                    this.city_input = '';
                    this.title_input = '';
                    this.parametersAccumulator = [];
                }
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