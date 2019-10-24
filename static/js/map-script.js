// загружаем координаты точек для яндекса
var vm_map = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app_map_points',
    data() {
        return {
            title: 'app_reestr_cok',
            direction: null,
            reestrCenters: [],
            search_parameters: {
                title: '',
                city: '',
            },
            accred_fields: {},
            qualification_checkboxes: []
        }
    },
    beforeMount() {
        console.log('1');
        this.check_local_storage_and_cookie();
        this.update_dirs();
    },
    mounted() {
        console.log('2');
    },
    methods: {
        update_dirs: function() {
            axios
            .get('/naks_api/dirs/')
            .then(response => {
                // console.log('response data', response.data[0]);
                var dirs = [{
                        'name': 'activity',
                        'plural': 'activities'
                    },
                    {
                        'name': 'weldtype',
                        'plural': 'weldtypes'
                    },
                    {
                        'name': 'level',
                        'plural': 'levels'
                    },
                    {
                        'name': 'gtu',
                        'plural': 'gtus'
                    },
                    {
                        'name': 'so_types',
                        'plural': 'so'
                    },
                    {
                        'name': 'sm_types',
                        'plural': 'sm'
                    }
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
                console.log('ready');
            })
        },
        check_local_storage_and_cookie: function() {
            let centers_updated_flag = this.$cookies.get("centers_storage_updated");
            if (localStorage.reestrCenters && centers_updated_flag) {
                this.reestrCenters = JSON.parse(localStorage.reestrCenters)
                this.map_render();
            } else {
                this.load_reestr_centers();
            }
            // console.log('reestr', this.reestrCenters.length, this.reestrCenters);
            console.log('this', this);
        },
        load_reestr_centers: function () {
            localStorage.clear();
            axios
                .get('/naks_api/centers/')
                .then(response => {
                    console.log('loading centers from api');
                    localStorage.reestrCenters = JSON.stringify(response.data);
                    this.reestrCenters = response.data;
                    this.$cookies.set("centers_storage_updated", "1", "1h");
                }).finally(() => {
                    console.log('rendering map...');
                    this.map_render();
                });
        },
        map_render: function() {
            ymaps.ready(this.map_init);
        },
        map_init: function() {
            let points = Array.from(this.reestrCenters.filter(element => element.active == true), function (item) {
                var org_obj = {
                    'coordinates': [item.coordinates[1], item.coordinates[0]],
                    'title': item.company,
                    'company_full_name': item.company_full_name,
                    'address': item.actual_address,
                    'direction': item.direction,
                    'short_code': item.short_code,
                    'id': item.id
                }
                return org_obj
            });
            var myMap = new ymaps.Map('map', {
                    center: [61.698653, 99.505405],
                    zoom: 3,
                    //МОЁ - убирает разные возможности карты, оставляя только zoom
                    controls: ['zoomControl']
                },
                {
                    searchControlProvider: 'yandex#search'
                }
                )
                // materials = 'attsm'
                // equipment = 'attso'
                // technologies = 'attst'
                // personal = 'personal'
                // csp = 'specpod'
                // qualification = 'qualifications'
                // certification = 'certification'
                let colors = {
                    'members': 'red',
                    'personal': 'red',
                    'attsm': 'cyan',
                    'attso': 'yellow',
                    'attst': 'green',
                    'qualifications': 'brown',
                    'specpod': 'darkcyan'
                };
                let objectManager = new ymaps.ObjectManager({
                    // Чтобы метки начали кластеризоваться, выставляем опцию.
                    clusterize: true,
                    // ObjectManager принимает те же опции, что и кластеризатор.
                    gridSize: 32,
                    clusterDisableClickZoom: true
                });
                let currentId = 0;
                var objects = [];
                for (var point of points) {
                  objects.push({
                        type:'Feature',
                        id: currentId++,
                        geometry: {
                            type: 'Point',
                            coordinates: point.coordinates
                        },
                        properties: {
                            clusterCaption: point.short_code,
                            hintContent: point.title,
                            balloonContent: point.company_full_name,
                        }
                    })
                }
                objectManager.add(objects);
                myMap.geoObjects.add(objectManager);

            // .add(new ymaps.Placemark([60.063119, 30.360002], {
            //     hintContent: 'ООО "РСЗ МАЦ"',
            //     balloonContent: '194292, город Санкт-Петербург, 3-й Верхний пер., д. 1, корп. 3, лит. С'
            // }, {
            //     iconColor: '#ED2629'
            // }))

            //МОЁ - чтобы при скролле странице, карта не масштабировалась
            myMap.behaviors.disable('scrollZoom');
        }
    }
})