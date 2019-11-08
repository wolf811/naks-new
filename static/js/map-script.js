// загружаем координаты точек для яндекса
var vm_map = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app_map_points',
    data() {
        return {
            title: 'app_reestr_map',
            show_map: 'sroMembers',
            sroMembers: [],
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
        this.getOrUpdateSroMembers();
        this.check_local_storage_and_cookie();
        this.update_dirs();
    },
    mounted() {
        console.log('Vue mounted');
        if (this.$refs.direction) {
            this.show_map = this.$refs.direction.dataset.direction;
            console.log('this show map', this.show_map);
        }

    },
    methods: {
        getOrUpdateSroMembers: function() {
            let sroMembersUpdatedFlag = this.$cookies.get("sro_members_updated");
            if (localStorage.reestrSroMembers && sroMembersUpdatedFlag) {
                this.sroMembers = JSON.parse(localStorage.reestrSroMembers);
            } else {
                axios
                    .get('/naks_api/sro-members/')
                    .then(response=> {
                        localStorage.reestrSroMembers = JSON.stringify(response.data);
                        var loaded_arr = JSON.parse(localStorage.reestrSroMembers);
                        this.sroMembers = loaded_arr;
                    })
                    .finally(()=>{
                        this.$cookies.set("sro_members_updated", "1", "1h");
                        console.log('finally sro_members updated');
                    })
            }
        },
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
                console.log('dirs updated by api');
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
        test_console: function(e) {
            e.preventDefault();
            console.log(this, 'click console');
        },
        map_init: function() {
            let select_objects = {
                'sroMembers': this.sroMembers,
                'allCenters': this.reestrCenters.filter(el=> el.active == true && el.direction != 'qualifications'),
                'allCoks': this.reestrCenters.filter(el=> el.active == true && el.direction == 'qualifications'),
                'allCertCenters': this.reestrCenters.filter(el => el.active == true && el.direction == 'certification'),
                'personal': this.reestrCenters.filter(el=>el.active == true && el.direction == 'personal'),
                'attsm': this.reestrCenters.filter(el=>el.active == true && el.direction == 'attsm'),
                'attso': this.reestrCenters.filter(el=>el.active == true && el.direction == 'attso'),
                'attst': this.reestrCenters.filter(el=>el.active == true && el.direction == 'attst'),
                'specpod': this.reestrCenters.filter(el=>el.active == true && el.direction == 'specpod'),
            };
            let points = [];
            if (this.show_map !== 'sroMembers') {
                points = Array.from(
                    select_objects[this.show_map], function (item) {
                    var point_obj = {
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
                    return point_obj
                })} else {
                    points = Array.from(
                        select_objects[this.show_map], function (item) {
                            var point_obj = {
                                'coordinates': [item.coordinates[1], item.coordinates[0]],
                                'short_name': item.short_name,
                                'full_name': item.full_name,
                                'company_full_name': item.company_full_name,
                                'address': item.actual_address,
                                'id': item.id,
                                'centers': item.centers,
                                'phone': item.phone,
                                'email': item.email
                            }
                            return point_obj
                        }
                    )
                }

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
                let point_directions = {
                    'personal': 'Аттестация персонала сварочного производства',
                    'attsm': 'Аттестация сварочных материалов',
                    'attso': 'Аттестация сварочного оборудования',
                    'attst': 'Атестация сварочных технологий',
                    'qualifications': 'Оценка квалификации в области сварки и контроля',
                    'specpod': 'Специальная подготовка персонала сварочного производства'
                }
                for (var point of points) {
                    let center_point_template = {
                        type:'Feature',
                        id: currentId++,
                        geometry: {
                            type: 'Point',
                            coordinates: point.coordinates,
                        },
                        properties: {
                            clusterCaption: point.short_code,
                            hintContent: point.title,
                            balloonContent: point.company_full_name,
                        }
                    };
                    let point_templates = {
                        'sroMembers': {
                            type:'Feature',
                            id: currentId++,
                            geometry: {
                                type: 'Point',
                                coordinates: point.coordinates
                            },
                            properties: {
                                clusterCaption: point.short_name,
                                hintContent: point.short_name,
                                balloonContent:
                                `
                                    ${point.full_name}<br>
                                    Адрес: ${point.address}<br>
                                    Телефон: ${point.phone}<br>
                                    E-mail: ${point.email}<br>
                                    Центры организации: ${point.centers}
                                `
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
                                    balloonContent:
                                    `
                                    Центр на базе: ${point.company_full_name}<br>
                                    Направление деятельности: ${point_directions[point.direction]}<br>
                                    <a href="#" class="map-btn-test btn btn-primary btn-xs mt-2">Подробнее</a>
                                    `,
                                }
                                // пример событий балуна и кластера
                                // https://tech.yandex.ru/maps/jsbox/2.1/event_rollover
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
                        'personal': center_point_template,
                        'attsm': center_point_template,
                        'attso': center_point_template,
                        'attst': center_point_template,
                        'specpod': center_point_template,
                    }
                  objects.push(point_templates[this.show_map])
                }
                objectManager.add(objects);
                if (this.show_map in {"allCenters":1, "allCoks": 1}) {
                    objectManager.objects.options.set({
                        preset: "islands#redIcon"
                        // Опции.
                           // Необходимо указать данный тип макета.
                        //    iconLayout: 'default#image',
                           // Своё изображение иконки метки.
                        //    iconImageHref: 'http://www.jonedmiston.com/wp-content/uploads/2012/09/octocat.png',
                           // Размеры метки.
                        //    iconImageSize: [30, 42],
                           // Смещение левого верхнего угла иконки относительно
                           // её "ножки" (точки привязки).
                        //    iconImageOffset: [-3, -42]
                   });
                   objectManager.clusters.options.set({
                        preset: 'islands#redClusterIcons'
                    });
                }
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
            this.map_render();
        }
    }
})