// загружаем координаты точек для яндекса
var vm_map = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app_map_points',
    data() {
        return {
            title: 'app_reestr_map',
            show_map: 'sroMembers',
            reestrCenters: [],
            accred_fields: {},
            qualification_checkboxes: [],
            search_parameters: {
                direction: '',
                levels: [],
                activities: [],
                weldtypes: [],
                gtus: [],
                sm_types: [],
                so_types: [],
                qualifications: []
            }
        }
    },
    beforeMount() {
        console.log('beforeMount');
        this.check_local_storage_and_cookie();
        this.update_dirs();
    },
    mounted() {
        console.log('Mounted');
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
            $('ymaps').remove();
            ymaps.ready(this.map_init);
        },
        map_init: function() {
            let unique_companies = Array.from(new Set(Array.from(this.reestrCenters.filter(el=> el.active == true), item=>item.company_full_name)));

            let select_objects = {
                'sroMembers': false,
                'allCenters': this.reestrCenters.filter(el=> el.active == true),
                'allCoks': this.reestrCenters.filter(el=> el.direction == 'qualifications'),
                'allCertCenters': this.reestrCenters.filter(el=> el.direction == 'certification')
            };
            let points = Array.from(select_objects[this.show_map], function (item) {
                var org_obj = {
                    'coordinates': [item.coordinates[1], item.coordinates[0]],
                    'title': item.company,
                    'company_full_name': item.company_full_name,
                    'address': item.actual_address,
                    'direction': item.direction,
                    'short_code': item.short_code,
                    'id': item.id,
                    'company': item.company,
                    'city': item.city,
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
                let objects = [];
                for (var point of points) {
                    let point_templates = {
                        'sroMembers': {
                            type:'Feature',
                            id: currentId++,
                            geometry: {
                                type: 'Point',
                                coordinates: point.coordinates
                            },
                            properties: {
                                clusterCaption: point.city,
                                hintContent: point.company,
                                balloonContent: point.company_full_name,
                            }
                        },
                        'allCenters': {
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
                            },
                        'allCoks': {
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
                                },
                                options: {
                                    fillColor: "0066ff99"
                                }
                            },
                        'allCertCenters': {
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
                            },
                    }
                  objects.push(point_templates[this.show_map])
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
        },
        buttonPress: function(parameter) {
            this.show_map = parameter
            switch (parameter) {
                case 'sroMembers':
                    console.log(parameter);
                    break;
                case 'allCenters':
                    console.log(parameter);
                    break;
                case 'allCoks':
                    console.log(parameter);
                    break;
                case 'allCertCenters':
                    console.log(parameter);
                    break;
                default:
                    break;
            }
            this.map_render();
            console.log('this show map', this.show_map);
        }
    }
})