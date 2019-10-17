if (document.getElementById('app_reestr_cok')) {
    var vm  = new Vue({
        delimiters: ['[[', ']]'],
        el: '#app_reestr_cok',
        data() {
            return {
                title: 'app_reestr_cok',
                direction: null,
                reestrCenters: [],
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
            }
        }
    })
}