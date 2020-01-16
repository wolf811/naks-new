// console.log('hello from vue js scripts');

// function arrayRemove(arr, value) {
//     return arr.filter( function(el) { return el != value; })
// }

var APP_LOG_LIFECYCLE_EVENTS = true;

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

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
                    activity: [],
                    gtu: [],
                    material: [],
                    so: [],
                    sm: [],
                },
            };
        },
        beforeMount() {
                axios
                    .get('/naks_api/dirs/')
                    .then(response => {
                    // console.log('response data', response.data[0]);
                        var dirs = [
                            {'name': 'activity', 'plural': 'activities'},
                            {'name': 'weldtype', 'plural': 'weldtypes'},
                            {'name': 'level', 'plural': 'levels'},
                            {'name': 'gtu', 'plural': 'gtus'},
                            {'name': 'so_types', 'plural': 'so'},
                            {'name': 'sm_types', 'plural': 'sm'}
                        ];
                        for (var dir of dirs) {
                            var reactive_arr = [];
                            for (var el of response.data[0][dir.plural]) {
                                var extended_el = el;
                                extended_el.selected = false;
                                extended_el.type = dir.name;
                                reactive_arr.push(extended_el);
                            }
                            // this.$set(this.accred_fields, dir.name, response.data[0][dir.plural]);
                            this.$set(this.accred_fields, dir.name, reactive_arr);
                        }
                    })
                    .finally(() => {
                        // console.log('beforeMount: api parameters loaded', this, 'weldtype', this.accred_fields.weldtype, 'weldtypes > 0:', this.accred_fields.weldtype.length > 0);
                        console.log('******************************************');
                        console.log('beforeMount: api parameters loaded', this);
                        console.log('******************************************');
                    });
        },
        mounted() {
            this.iamhere();
        },
        watch: {
            selected: {
                handler: function(newVal, oldVall) {
                    {}
                    // console.log('selected changed', newVal);
                    // this.selected_lengths_sum();
                },
                deep: true
            }
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
            },
            log_change: function() {
                console.log('changes', this);
            },
            selected_lengths_sum: function() {
                var sum_length = 0;
                for (var key of Object.keys(this.selected)) {
                    sum_length+=this.selected[key].length;
                }
                return sum_length
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
                    console.log('parameters', this.parametersAccumulator);
                }
                var result_array = [];



                for (var element of this.reestrCenters) {
                    var passing = true;
                    for (var p of this.parametersAccumulator) {
                        var parameter = p.parameter;
                        var value = p.value;
                        if (parameter in {"city":1, "short_code": 1}) {
                            if (!element[p.parameter].toUpperCase().includes(value.toUpperCase())) {
                                passing = false;
                                break;
                            }
                        }
                        if (parameter in {"special_gp": 1, "special_tn": 1}) {
                            if (value == false) {
                                continue;
                            } else {
                                if (element[p.parameter] != value) {
                                    passing = false;
                                    break;
                                }
                            }
                        }
                        if (parameter in {"gtus": 1, "so_types": 1}) {
                            // {'parameter': 'gtus', 'value': gtu_id_arr};
                            // each of value: {'id': item.id, 'parent': item.parent}
                            // console.log('element', element, element[parameter])
                            for (var item of value) {
                                var searching = null;
                                item.parent == null ? searching = item.id : searching = item.parent;

                                if (!element[parameter].includes(searching)) {
                                    passing = false;
                                }
                            }
                        }
                        if (parameter in {'weldtypes': 1, 'activities': 1, 'levels': 1, 'sm_types': 1}) {
                            // console.log('searching activities', input_data);
                            for (var item of value) {
                                if (!element[parameter].includes(item)) {
                                    passing = false;
                                }
                            }
                        }
                    }
                    if (passing) {
                        result_array.push(element);
                    }
                }
                console.log('parameter', parameter, value)
                this.on_screen = result_array.filter(el => el.direction == this.direction);
                console.log('result', this.on_screen, this.on_screen.length)
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
                this.parametersAccumulator = [];
                this.on_screen = [];
                this.special_tn = false;
                this.special_gp = false;
                if (this.city_input.length != 0 || this.title_input.length !=0) {
                    this.city_input = '';
                    this.title_input = '';
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
                for (var key of Object.keys(this.selected)) {
                    this.selected[key] = [];
                }

                var selected_checkboxes_arr = this.accred_fields.gtu
                    .concat(this.accred_fields.weldtype)
                    .concat(this.accred_fields.level)
                    .concat(this.accred_fields.activity)
                    .concat(this.accred_fields.sm_types)
                    .concat(this.accred_fields.so_types)
                for (var el of selected_checkboxes_arr) {
                    el.selected = false;
                }
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
            selectLevel: function(item) {
                var selected_levels = Array.from(this.accred_fields.level.filter(lv => lv.selected == true), function(item) {
                    return item.id;
                });
                this.selected.level = selected_levels;
                this.filterByInput({'parameter': 'levels', 'value': selected_levels});
            },
            selectActivities: function (item) {
                var selected_activities = Array.from(this.accred_fields.activity.filter(act => act.selected == true), function(item){
                    return item.id;
                });
                this.selected.activity = selected_activities;
                this.filterByInput({'parameter': 'activities', 'value': selected_activities});
            },
            selectWeldtype: function(item) {
                var selected_weldtypes = Array.from(this.accred_fields.weldtype.filter(wt => wt.selected == true), function(item){
                    return item.id;
                });
                this.selected.weldtype = selected_weldtypes;
                this.filterByInput({'parameter': 'weldtypes', 'value': selected_weldtypes});
            },
            selectGtu: function(item) {
                for (var el of this.accred_fields.gtu) {
                    if (el === item) {
                        continue;
                    } else {
                        el.parent === item.id ? el.selected = item.selected : null;
                    }
                }
                var gtu_id_arr = Array.from(this.accred_fields.gtu.filter(el => el.selected == true), function(item) {
                    return {'id': item.id, 'parent': item.parent}
                });
                this.selected.gtu = gtu_id_arr;
                this.filterByInput({'parameter': 'gtus', 'value': gtu_id_arr});
            },
            selectEquipment: function(item) {
                for (var el of this.accred_fields.so_types) {
                    if (el === item ) {
                        continue;
                    } else {
                        el.parent === item.id ? el.selected = item.selected: null;
                    }
                }
                var so_id_arr = Array.from(this.accred_fields.so_types.filter(el => el.selected == true), function(item) {
                    return {'id': item.id, 'parent': item.parent}
                });
                this.selected.so = so_id_arr;
                this.filterByInput({'parameter': 'so_types', 'value': so_id_arr})
            },
            selectMaterial: function(item) {
                let sm_id_arr = Array.from(this.accred_fields.sm_types.filter(el => el.selected == true), function(item){
                    return item.id
                })
                this.selected.sm = sm_id_arr;
                this.filterByInput({'parameter': 'sm_types', 'value': sm_id_arr})
            },
            saveSearch: function() {
                if (this.on_screen.length > 0) {
                    this.show_filtered(this.on_screen);
                    this.show_hidden_centers();
                    this.make_tables_unstriped();
                }
            },
            change_input_deprecated: function(input) {
                input.selected = !input.selected;
                this.selected[input.type] = this.filter_selected_inputs(this.accred_fields[input.type]);
            },
            filter_selected_inputs: function(input_arr) {
                if (input_arr.length > 0) {
                    var filtered = input_arr.filter(element => element.selected == true);
                    return filtered;
                } else {
                    return [];
                }
            }
        },

    });
}

if (document.getElementById('app_registry_personal')) {
    var vm_registry_personal = new Vue({
        delimiters: ['[[', ']]'],
        el: '#app_registry_personal',
        data() {
            return {
                selected_activities: {},
                stamp_input: '',
                fio_input: '',
                company_input: '',
                place_of_att__center: null,
                place_of_att__point: null,
                accred_fields: {},
                searchResultHTML: null,
                centersAndPoints: [],
                reestrCenters: [],
                selectedCenter: '',
                selectedCenterPoints: []
            }
        },
        beforeMount() {
            this.check_local_storage_and_cookie();
            this.update_dirs();
        },
        methods: {
            check_local_storage_and_cookie: function () {
                let centers_updated_flag = this.$cookies.get("centers_storage_updated");
                if (localStorage.reestrCenters && centers_updated_flag) {
                    this.reestrCenters = JSON.parse(localStorage.reestrCenters)
                } else {
                    this.load_reestr_centers();
                }
            },
            load_reestr_centers: function () {
                localStorage.clear();
                axios
                    .get('/naks_api/centers/')
                    .then(response => {
                        localStorage.reestrCenters = JSON.stringify(response.data);
                        this.reestrCenters = response.data;
                        this.$cookies.set("centers_storage_updated", "1", "1h");
                    }).finally(() => {
                        // console.log('rendering map...');
                        this.map_render();
                    });
            },
            update_dirs: function() {
                axios
                .get('/naks_api/dirs/')
                .then(response => {
                // console.log('response data', response.data[0]);
                    var dirs = [
                        {'name': 'activity', 'plural': 'activities'},
                        {'name': 'weldtype', 'plural': 'weldtypes'},
                        {'name': 'level', 'plural': 'levels'},
                        {'name': 'gtu', 'plural': 'gtus'},
                        {'name': 'so_types', 'plural': 'so'},
                        {'name': 'sm_types', 'plural': 'sm'}
                    ];
                    for (var dir of dirs) {
                        var reactive_arr = [];
                        for (var el of response.data[0][dir.plural]) {
                            var extended_el = el;
                            extended_el.selected = false;
                            extended_el.type = dir.name;
                            reactive_arr.push(extended_el);
                        }
                        // this.$set(this.accred_fields, dir.name, response.data[0][dir.plural]);
                        this.$set(this.accred_fields, dir.name, reactive_arr);
                    }
                })
                .finally(() => {
                    // console.log('beforeMount: api parameters loaded', this, 'weldtype', this.accred_fields.weldtype, 'weldtypes > 0:', this.accred_fields.weldtype.length > 0);
                    console.log('******************************************');
                    console.log('beforeMount: api parameters loaded', this);
                    console.log('******************************************');
                });
            },
            selectGtu: function (item) {
                item = null;
            },
            sendSearchRequest: function() {
                let payload = new FormData();
                payload.append("search_request", "i am searching!");
                axios
                    .post('/registry/personal/', payload)
                    .then(response => {
                        // console.log(response.data);
                        this.searchResultHTML = response.data;
                        // console.log(response);

                    })
                    .catch( error => {
                        console.log(error);
                    })
                    .finally( ()=>{
                        console.log('finnally sendSearchRequest');
                    })
            },
            resetSearchQuery: function() {
                this.searchResultHTML = null;
            }
        },
        computed: {
            getAttPlaces: function() {
                let centers = this.reestrCenters;
                let resulting = {}
                for cnt in centers.filter(item=>{
                    item.direction == 'personal' && item.active = true;
                })

                return centers
            }
        }
    })
    console.log('reestr here')
}