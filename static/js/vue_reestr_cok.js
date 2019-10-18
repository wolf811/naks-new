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
                search_parameters: {
                    title: '',
                    city: '',
                    qualifications: [],
                },
            }
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
            console.log('reestr', this.reestrCenters.length, this.reestrCenters);
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
        },
        computed: {
            filteredCenters: function() {
                let search_parameters = this.search_parameters;
                console.log('filtering...', search_parameters);
                let centers = this.reestrCenters;
                let search_title_string = this.title_input.trim().toLowerCase();

                let show_full_reestr = true;
                for (var key of Object.keys(this.search_parameters)) {
                    console.log('key', key, key, search_parameters[key].length);
                    if (search_parameters[key].length > 0) {
                        show_full_reestr = false;
                    }
                }
                if (show_full_reestr) {
                    return centers;
                }


                centers = centers.filter(function(item){
                    return (item.company.includes(search_parameters.title) ||
                            item.short_code.includes(search_parameters.title)) &&
                            item.city.includes(search_parameters.city) &&
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

                // centers = centers.filter(function(item) {
                //     if (item.short_code.toLowerCase().indexOf(search_title_string) !== -1 ||
                //     item.company.toLowerCase().indexOf(search_title_string) !== -1) {
                //         return item;
                //     }
                // })
                // return centers
            }
        }
    })
}