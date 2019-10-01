// console.log('hello from vue js scripts');

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
    var vm = new Vue({
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
                parametersAccumulator: [],
                accred_fields: {},
                selected: {
                    level: [],
                    weldtype: [],
                    gtu: [],
                    material: [],
                    equipment: [],
                },
            };
        },
        beforeMount() {
                axios
                    .get('/naks_api/dirs/')
                    .then(response => {
                    // console.log('response', response.data, 'levels', response.data[0].levels);
                    this.$set(this.accred_fields, 'level', response.data[0].levels);
                    for (var lv of this.accred_fields.level) {
                        lv.selected = false;
                        lv.type = 'level';
                    }
                    console.log('beforeMount: api parameters loaded', this, 'level', this.accred_fields.level, 'levels > 0:', this.accred_fields.level.length > 0);
                });
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
                } else {
                    this.load_reestr_centers();
                }
                console.log('i am here', this);
            },
            log_change: function() {
                console.log('changes', this);
            },
            load_form_parameters: function() {
                console.log('loading dir parameters from api');
                axios
                    .get('/naks_api/dirs/')
                    .then(response => {
                        this.accred_fields.levels = response.data[0].levels;
                        console.log('updated Vue', this, 'levels', this.accred_fields.levels, this.accred_fields.levels.length);
                    });
                console.log('api parameters loaded');
            },
            load_reestr_centers: function() {
                localStorage.clear();
                axios
                .get('/naks_api/centers/')
                .then(response => {
                    console.log('loading centers from api');
                    localStorage.reestrCenters = JSON.stringify(response.data);
                    var loaded_arr = JSON.parse(localStorage.reestrCenters);
                    this.$cookies.set("centers_storage_updated", "1", "1h");
                    this.reestrCenters = loaded_arr.filter(element => element.direction == this.direction);
                    });
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
            onSpecialsTnChekbox: function() {
                    // console.log('special tn', this.special_tn);
                        this.filterByInput({'parameter': 'special_tn', 'value': this.special_tn});
                        this.show_filtered(this.on_screen);
                        this.show_hidden_centers();
                        this.make_tables_unstriped();
            },
            onSpecialsGpChekbox: function() {
                    // console.log('special gp');
                        this.filterByInput({'parameter': 'special_gp', 'value': this.special_gp});
                        this.show_filtered(this.on_screen);
                        this.show_hidden_centers();
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
                    // console.log('parameters', this.parametersAccumulator);
                }
                var result_array = [];


                for (var element of this.reestrCenters) {
                    var passing = true;
                    for (var param of this.parametersAccumulator) {
                        if (param.parameter in {"city":1, "short_code": 1}) {
                            if (!element[param.parameter].toUpperCase().includes(param.value.toUpperCase())) {
                                passing = false;
                                break;
                            }
                        }
                        if (param.parameter in {"special_gp": 1, "special_tn": 1}) {
                            if (param.value == false) {
                                continue;
                            } else {
                                if (element[param.parameter] != param.value) {
                                    passing = false;
                                    break;
                                }
                            }
                        }
                    }
                    if (passing) {
                        result_array.push(element);
                    }
                }
                // console.log('result_array', result_array.filter(el => el.direction == this.direction));
                this.on_screen = result_array.filter(el => el.direction == this.direction);

            },
            show_filtered: function(arr) {
                // console.log('to show', arr);
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
                this.on_screen = [];
                this.special_tn = false;
                this.special_gp = false;
            },
            make_tables_unstriped: function() {
                var tables = document.querySelectorAll('table');
                for (var table of tables) {
                    $(table).removeClass('table-striped');
                }
            },
            server_search: function() {
                let data = new FormData()
                let attrs = {
                    'city': this.city_input,
                    'short_code': this.title_input,
                    'special_tn': this.special_tn,
                    'special_gp': this.special_gp
                }
                for (const [key, value] of Object.entries(attrs)) {
                    data.append(key, value);
                }
                axios
                    .post(`/reestr/centers/${this.direction}`, data)
                    .then(response=> {console.log('server_response', response.data)})
            },
            change_input: function(input) {
                input.selected = !input.selected;
                this.selected[input.type] = this.filter_selected_inputs(this.accred_fields[input.type]);
                console.log('change input', this, 'input', input);
            },
            filter_selected_inputs: function(input_arr) {
                if (input_arr.length > 0) {
                    var filtered = input_arr.filter(element => element.selected == true);
                    console.log('counting inputs', filtered, filtered.length);
                    return filtered;
                } else {
                    return [];
                }
            }
        },

    });
}