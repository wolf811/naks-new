// загружаем координаты точек для яндекса
if ($('#app_map_points').length != 0) {
    var vm_map = new Vue({
        delimiters: ['[[', ']]'],
        el: '#app_map_points',
        data() {
            return {
                title: 'app_reestr_map',
                show_map: 'sroMembers',
                sroMembers: [],
                filteredCenters: [],
                directions: [
                    {
                        code: 'personal',
                        title: '<span class="badge badge-info">АЦСП</span> Центры по аттестации персонала',
                        selected: false
                    },
                    {
                        code: 'specpod',
                        title: '<span class="badge badge-info">ЦСП</span> Центры специальной подготовки',
                        selected: false
                    },
                    {
                        code: 'attsm',
                        title: '<span class="badge badge-info">АЦСМ</span> Центры по аттестации сварочных материалов',
                        selected: false
                    },
                    {
                        code: 'attso',
                        title: '<span class="badge badge-info">АЦСО</span> Центры по аттестации сварочного оборудования',
                        selected: false
                    },
                    {
                        code: 'attst',
                        title: '<span class="badge badge-info">АЦСТ</span> Центры по аттестации сварочных технологий',
                        selected: false
                    },
                    {
                        code: 'qualifications',
                        title: '<span class="badge badge-info">ЦОК</span> Центры оценки квалификаций',
                        selected: false
                    },
                    // {
                    //     code: 'certification',
                    //     title: '<span class="badge badge-info">ОСП</span> Органы сертификации сварочного производства',
                    //     selected: false
                    // }
                ],
                reestrCenters: [],
                accred_fields: {},
                obldObject: {},
                qualification_checkboxes: [],
                search_parameters: {
                    directions: [],
                    levels: [],
                    activities: [],
                    weldtypes: [],
                    gtus: [],
                    sm_types: [],
                    so_types: [],
                    qualifications: []
                },
                fieldSet: {
                    'personal': ['levels', 'activities', 'gtus', 'weldtypes'],
                    'attsm': ['sm_types', 'gtus'],
                    'attso': ['gtus', 'so_types'],
                    'attst': ['gtus', 'weldtypes'],
                    'qualifications': ['qualifications'],
                    'specpod': ['levels', 'weldtypes', 'gtus'],
                },
            }
        },
        beforeMount() {
            this.getOrUpdateSroMembers();
            this.check_local_storage_and_cookie();
            this.update_dirs();
            // this.getDirections();
        },
        mounted() {
            // inner pages maps checking for direction of activity
            // takes direction from ref on page
            if (this.$refs.direction) {
                this.show_map = this.$refs.direction.dataset.direction;
            }
        },
        methods: {
            getDirections: function () {
                let direction_titles = {
                    'personal': 'Центры по аттестации персонала (АЦ)',
                    'specpod': 'Центры специальной подготовки (ЦСП)',
                    'attsm': 'Центры по аттестации сварочных материалов (АЦСМ)',
                    'attso': 'Центры по аттестации сварочного оборудования (АЦСО)',
                    'attst': 'Центры по аттестации сварочных технологий (АЦСТ)',
                    'qualifications': 'Центры оценки квалификаций (ЦОК)',
                    'certification': 'Органы сертификации сварочного производства (ОСП)'
                }
                for (var center of this.reestrCenters) {
                    let direction = center.direction;
                    !(direction in this.directions) ? this.directions[direction] = direction_titles[direction]: null;
                }
            },
            makeObldObject: function() {
                for (var key of Object.keys(this.accred_fields)) {
                    for (var value of this.accred_fields[key]) {
                        key == 'level' ?
                            this.obldObject[value.id] = {short_name: value.level, full_name: value.level+' уровень'} :
                            this.obldObject[value.id] = {short_name: value.short_name, full_name: value.full_name}
                    }
                }
            },
            getOrUpdateSroMembers: function () {
                let sroMembersUpdatedFlag = this.$cookies.get("sro_members_updated");
                if (localStorage.reestrSroMembers && sroMembersUpdatedFlag) {
                    this.sroMembers = JSON.parse(localStorage.reestrSroMembers);
                } else {
                    axios
                        .get('/naks_api/sro-members/')
                        .then(response => {
                            localStorage.reestrSroMembers = JSON.stringify(response.data);
                            var loaded_arr = JSON.parse(localStorage.reestrSroMembers);
                            this.sroMembers = loaded_arr;
                        })
                        .finally(() => {
                            this.$cookies.set("sro_members_updated", "1", "1h");
                            console.log('finally sro_members updated');
                        })
                }
            },
            update_dirs: function () {
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
                            },
                            {
                                'name': 'qualifications',
                                'plural': 'qualifications'
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
                        console.log('dirs updated by api', this.accred_fields);
                        this.qualification_checkboxes = this.accred_fields.qualifications;
                        this.makeObldObject();
                    })
            },
            check_local_storage_and_cookie: function () {
                let centers_updated_flag = this.$cookies.get("centers_storage_updated");
                if (localStorage.reestrCenters && centers_updated_flag) {
                    this.reestrCenters = JSON.parse(localStorage.reestrCenters)
                    this.map_render();
                } else {
                    this.load_reestr_centers();
                }
                // console.log('reestr', this.reestrCenters.length, this.reestrCenters);
                // console.log('this', this);
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
            map_render: function () {
                $('ymaps').remove();
                ymaps.ready(this.map_init);
            },
            map_init: function () {
                let select_objects = {
                    'sroMembers': this.sroMembers,
                    'filtered': this.filteredCenters,
                    'allCenters': this.reestrCenters.filter(el => el.active == true && el.direction != 'qualifications'),
                    'allCoks': this.reestrCenters.filter(el => el.active == true && el.direction == 'qualifications'),
                    'allCertCenters': this.reestrCenters.filter(el => el.active == true && el.direction == 'certification'),
                    'personal': this.reestrCenters.filter(el => el.active == true && el.direction == 'personal'),
                    'attsm': this.reestrCenters.filter(el => el.active == true && el.direction == 'attsm'),
                    'attso': this.reestrCenters.filter(el => el.active == true && el.direction == 'attso'),
                    'attst': this.reestrCenters.filter(el => el.active == true && el.direction == 'attst'),
                    'specpod': this.reestrCenters.filter(el => el.active == true && el.direction == 'specpod'),
                };
                let points = [];
                // function test(item) {
                //     var string = '';
                //     for (var key of this.fieldSet[item.direction]) {
                //         string+=item[key];
                //     }
                //     return string;
                // }
                var search_parameters = this.search_parameters;
                var fieldSet = this.fieldSet;
                var obldObject = this.obldObject;
                var resulting_arr = [];
                for (var val of Object.values(search_parameters)) {
                    if (val.length > 0 && typeof val[0] === 'object') {
                        for (var el of val) {
                            resulting_arr.push(el.id);
                        }
                    }
                }
                // console.log('resulting arr', resulting_arr);
                if (this.show_map !== 'sroMembers') {
                    points = Array.from(
                        select_objects[this.show_map],
                        function (item) {
                            function get_obl(point) {
                                var string = '';
                                for (var key of fieldSet[point.direction]) {
                                    for (var id of point[key]) {
                                        // Object.keys(search_parameters).reduce(function(res, v) {
                                        //     return res.concat(search_parameters[v]);
                                        // }, []).includes(id)
                                        resulting_arr.includes(id) ?
                                        string+=' <strong class="text-danger">'+obldObject[id].short_name + '</strong>':
                                        string+=' '+obldObject[id].short_name
                                    }
                                }
                                return string;
                            }
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
                                'oblD': get_obl(item),

                            }
                            return point_obj
                        })
                } else {
                    points = Array.from(
                        select_objects[this.show_map],
                        function (item) {
                            var point_obj = {
                                'coordinates': [item.coordinates[1], item.coordinates[0]],
                                'short_name': item.short_name,
                                'full_name': item.full_name,
                                'company_full_name': item.company_full_name,
                                'address': item.actual_address,
                                'id': item.id,
                                'centers': item.centers,
                                'phone': item.phone,
                                'email': item.email,
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
                }, {
                    searchControlProvider: 'yandex#search'
                })
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
                    'specpod': 'Специальная подготовка персонала сварочного производства',
                }
                for (var point of points) {
                    let center_point_template = {
                        type: 'Feature',
                        id: currentId++,
                        geometry: {
                            type: 'Point',
                            coordinates: point.coordinates,
                        },
                        properties: {
                            clusterCaption: point.short_code,
                            hintContent: point.title,
                            balloonContent: `
                            ${point.company_full_name}<br>
                            Область деятельности: ${point.oblD}
                            `,
                        }
                    };
                    let point_templates = {
                        'sroMembers': {
                            type: 'Feature',
                            id: currentId++,
                            geometry: {
                                type: 'Point',
                                coordinates: point.coordinates
                            },
                            properties: {
                                clusterCaption: point.short_name,
                                hintContent: point.short_name,
                                balloonContent: `
                                        ${point.full_name}<br>
                                        Адрес: ${point.address}<br>
                                        Телефон: ${point.phone}<br>
                                        E-mail: ${point.email}<br>
                                        Центры организации: ${point.centers}
                                    `
                            }
                        },
                        'allCenters': {
                            type: 'Feature',
                            id: currentId++,
                            geometry: {
                                type: 'Point',
                                coordinates: point.coordinates
                            },
                            properties: {
                                clusterCaption: point.short_code,
                                hintContent: point.title,
                                balloonContent: `
                                        Центр на базе: ${point.company_full_name}<br>
                                        Направление деятельности: ${point_directions[point.direction]}<br>
                                        <a href="#" class="map-btn-test btn btn-primary btn-xs mt-2">Подробнее</a>
                                        `,
                            }
                            // пример событий балуна и кластера
                            // https://tech.yandex.ru/maps/jsbox/2.1/event_rollover
                        },
                        'allCoks': {
                            type: 'Feature',
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
                            type: 'Feature',
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
                        'filtered': center_point_template,
                    }
                    objects.push(point_templates[this.show_map])
                }
                objectManager.add(objects);
                if (this.show_map in {
                        "allCenters": 1,
                        "allCoks": 1
                    }) {
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
            buttonPress: function (parameter) {
                this.show_map = parameter
                this.map_render();
                this.resetMapSearch(render=false);
            },
            selectDirection: function () {
                // console.log('direction selected', item);
                this.search_parameters.directions = Array.from(this.directions.filter(el=>el.selected==true), function(item) {
                    return item.code;
                });
            },
            selectLevel: function (item) {
                console.log('selected levels', item);
                this.search_parameters.levels = this.accred_fields.level.filter(element => element.selected === true);
            },
            selectActivities: function (item) {
                this.search_parameters.activities= this.accred_fields.activity.filter(element => element.selected === true);
                console.log('activity selected', item);
            },
            selectWeldtype: function (item) {
                this.search_parameters.weldtypes = this.accred_fields.weldtype.filter(element => element.selected === true);
            },
            selectGtu: function (item) {
                this.search_parameters.gtus= this.accred_fields.gtu.filter(element => element.selected === true);
                console.log('gtu selected', item);
            },
            selectEquipment: function (item) {
                this.search_parameters.so_types = this.accred_fields.so_types.filter(element => element.selected === true);
                console.log('equipment selected', item);
            },
            selectMaterial: function (item) {
                this.search_parameters.sm_types = this.accred_fields.sm_types.filter(element => element.selected === true);
                console.log('materials selected', item);
            },
            selectQual: function (item) {
                this.search_parameters.qualifications = this.qualification_checkboxes.filter(element => element.selected === true);
                console.log('qualification selected', item);
            },
            resetMapSearch: function(render=true) {
                for (var key of Object.keys(this.search_parameters)) {
                    this.search_parameters[key] = [];
                }
                for (var direction of this.directions) {
                    direction.selected = false;
                }
                for (var field of Object.keys(this.accred_fields)) {
                    for (var el of this.accred_fields[field]) {
                        el.selected = false;
                    }
                }
                $('#collapseAccordFilterAc_centrs').addClass('show');
                if (render) {
                    this.show_map = 'sroMembers';
                    this.map_render();
                }
            },
            saveMapSearch: function() {
                console.log('save search pressed');
                this.show_map = 'filtered';
                this.filterCenters();
                this.map_render();
                // filter_results
            },
            filterCenters: function() {
                let centers = this.reestrCenters;
                let search_parameters = this.search_parameters;
                let show_full_reestr = true;
                for (var key of Object.keys(search_parameters)) {
                    if (search_parameters[key].length > 0) {
                        show_full_reestr = false;
                    }
                }
                if (show_full_reestr) {
                    this.filteredCenters = centers;
                    console.log('showing full reestr');
                    return
                } else {
                    var fieldset = this.fieldSet;
                    centers = centers.filter(center => {
                        if (search_parameters['directions'].length > 0 &&
                            Object.keys(search_parameters)
                            .filter(el=>el !== 'directions')
                            .every(arr => search_parameters[arr].length == 0)) {
                                return search_parameters['directions'].includes(center.direction) && center.active == true;
                            }
                        var center_fields = fieldset[center.direction];
                        var search_fields = Object.keys(search_parameters).filter(el=>search_parameters[el].length > 0 && center_fields.includes(el));
                        return search_parameters.directions.includes(center.direction) && center.active == true &&
                            function() {
                                var passing = true;
                                for (var field of search_fields) {
                                    // if (search_parameters[field].length > 0 && search_parameters[field].every(el=>center[field].includes(el.id))) {
                                    if (!search_parameters[field].every(el=>center[field].includes(el.id))) {
                                        passing = false;
                                        // console.log('not match', center.company, field, center[field]);
                                        break;
                                    }
                                }
                                // console.log('match', center.short_code, center, field, center[field]);
                                return passing;
                            }();
                    });
                    // console.log('filtered centers', centers);

                    this.filteredCenters = centers;
                }
            },

        },
        computed: {
            search_parameters_length: function() {
                let sum = 0;
                for (var key of Object.keys(this.search_parameters)) {
                    sum+=this.search_parameters[key].length;
                }
                return sum
            }
        },
    })
}