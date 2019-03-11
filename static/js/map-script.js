// Яндекс Карта
ymaps.ready(init);

function init () {
    var myMap = new ymaps.Map('map', {
        center: [61.698653, 99.505405],
        zoom: 3,
                //МОЁ - убирает разные возможности карты, оставляя только zoom
                controls: ['zoomControl'] 
            }, {
                searchControlProvider: 'yandex#search'
            }),
    objectManager = new ymaps.ObjectManager({
            // Чтобы метки начали кластеризоваться, выставляем опцию.
            clusterize: true,
            // ObjectManager принимает те же опции, что и кластеризатор.
            gridSize: 32,
            clusterDisableClickZoom: true
        });

    myMap.geoObjects
    .add(new ymaps.Placemark([55.664756, 37.752464], {
        hintContent: 'СРО НП "НАКС"',
        balloonContent: 'Москва, ул. Братиславская, 6, эт. 4, под. 4'
    }, {
        iconColor: '#ED2629'
    }))
    .add(new ymaps.Placemark([60.063119, 30.360002], {
        hintContent: 'ООО "РСЗ МАЦ"',
        balloonContent: '194292, город Санкт-Петербург, 3-й Верхний пер., д. 1, корп. 3, лит. С'
    }, {
        iconColor: '#ED2629'
    }))
    .add(new ymaps.Placemark([55.131295, 61.374122], {
        hintContent: 'ООО "Центр подготовки специалистов "Сварка и Контроль"',
        balloonContent: '454087, город Челябинск, улица Рылеева, дом 11'
    }, {
        iconColor: '#ED2629'
    }))
    .add(new ymaps.Placemark([61.272337, 73.412014], {
        hintContent: 'ООО Аттестационный центр "НАКС - Западная Сибирь"',
        balloonContent: '628407, Ханты-Мансийский Автономный округ - Югра АО, город Сургут, улица Технологическая, дом 1'
    }, {
        iconColor: '#ED2629'
    }))
    .add(new ymaps.Placemark([48.526213, 135.069348], {
        hintContent: 'ООО Аттестационный центр "НАКС-Хабаровск"',
        balloonContent: '680009, город Хабаровск, переулок Бородинский, дом 1'
    }, {
        iconColor: '#ED2629'
    }))
    .add(new ymaps.Placemark([53.065160, 158.632804], {
        hintContent: 'ООО Научно-производственное предприятие "КОМПЛЕКС"',
        balloonContent: '683031, Камчатский край, город Петропавловск-Камчатский, проспект Карла Маркса, дом 11 А'
    }, {
        iconColor: '#ED2629'
    }));

    // Чтобы задать опции одиночным объектам и кластерам,
    // обратимся к дочерним коллекциям ObjectManager.
    objectManager.objects.options.set('preset', 'islands#greenDotIcon');
    objectManager.clusters.options.set('preset', 'islands#greenClusterIcons');
    myMap.geoObjects.add(objectManager);

    //МОЁ - чтобы при скролле странице, карта не масштабировалась
    myMap.behaviors.disable('scrollZoom'); 

    // Добавление меток через .json
    // $.ajax({
    //     url: "data.json"
    // }).done(function(data) {
    //     objectManager.add(data);
    // });
}

// окончание скриптов карты