if (document.getElementById('app_reestr_cok')) {
    var vm  = new Vue({
        delimiters: ['[[', ']]'],
        el: '#app_reestr_cok',
        data() {
            return {
                title: 'app_reestr_cok',
                direction: null,
                reestrCenters: [],
                title_input: '',
                city_input: '',
                qualification_checkboxes: null,
                search_parameters: {
                    title: '',
                    city: '',
                    qualifications: [],
                },
            }
        },
        beforeMount() {
            axios
                .get('/naks_api/dirs/')
                .then(response=>{
                    let reactive_arr = [];
                    let qualifications = response.data[0].qualifications;
                    // console.log('qualifications from api', qualifications);
                    for (var qual of qualifications) {
                        let qual_obj = qual;
                        qual_obj.selected = false;
                        reactive_arr.push(qual_obj);
                    }
                    this.qualification_checkboxes = reactive_arr;
                    // this.$set('qualification_checkboxes', reactive_arr);
                })
                .finally(()=> {
                    console.log('qualification dirs loaded');
                })
        },
        mounted() {
            this.direction = this.$refs.direction.dataset.direction;
            let centers_updated_flag = this.$cookies.get("centers_storage_updated");
            if (localStorage.reestrCenters && centers_updated_flag) {
                    this.reestrCenters = JSON.parse(localStorage.reestrCenters).filter(element => {
                        return element.direction.includes(this.direction);
                    });
            } else {
                this.load_reestr_centers();
            }
            // console.log('reestr', this.reestrCenters.length, this.reestrCenters);
            console.log('this', this);
        },
        methods: {
            load_reestr_centers: function() {
                localStorage.clear();
                axios
                .get('/naks_api/centers/')
                .then(response => {
                    console.log('loading centers from api');
                    localStorage.reestrCenters = JSON.stringify(response.data);
                    let loaded_arr = JSON.parse(localStorage.reestrCenters);
                    this.$cookies.set("centers_storage_updated", "1", "1h");
                    this.reestrCenters = loaded_arr.filter(element => element.direction.includes(this.direction));
                    });
            },
            selectQual: function(item) {
                for (var el of this.qualification_checkboxes) {
                    if (el.parent === item.id) {
                        el.selected = item.selected;
                    }
                }
                let qual_selected_arr = Array.from(this.qualification_checkboxes.filter(el => el.selected == true), function(item){
                    return item.id
                })
                this.search_parameters.qualifications = qual_selected_arr;

                // console.log('selected quals', this.qualification_checkboxes);
                // console.log('parameters', this.search_parameters);
            },
            saveSearch: function() {
                console.log('saved search');
            },
            resetSearch: function() {
                this.search_parameters = {
                    title: '',
                    city: '',
                    qualifications: [],
                }
                for (el of this.qualification_checkboxes) {
                    el.selected = false;
                }
            }
        },
        computed: {
            filteredCenters: function() {
                let search_parameters = this.search_parameters;
                // console.log('filtering...', search_parameters);
                let centers = this.reestrCenters;

                let show_full_reestr = true;
                for (var key of Object.keys(this.search_parameters)) {
                    // console.log('key', key, key, search_parameters[key].length);
                    if (search_parameters[key].length > 0) {
                        show_full_reestr = false;
                    }
                }
                if (show_full_reestr) {
                    return centers;
                }

                centers = centers.filter(function(item){
                    return (item.company.toLowerCase().includes(search_parameters.title.toLowerCase()) ||
                            item.short_code.toLowerCase().includes(search_parameters.title.toLowerCase())) &&
                            item.city.toLowerCase().includes(search_parameters.city.toLowerCase()) &&
                            function(){
                                for (var el of search_parameters.qualifications) {
                                    if (!item.qualifications.includes(el)) {
                                        return false
                                    }
                                }
                                return true
                            }();
                })
                return centers
            }
        }
    })
}