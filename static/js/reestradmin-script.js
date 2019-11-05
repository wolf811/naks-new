$(document).ready(() => {
    $(function() {
        $('[data-toggle="popover"]').popover();
        $('[data-toggle="tooltip"]').tooltip();
    });

    // TODO: focus for button-butter
    $('.navbar-toggler').click(function() {
        $(this).toggleClass('navbar-toggler-focus');
    });

    // TODO: change forms for document types
    $('.list-group-item-action').click(function(event) {
        var target = $(event.target);
        var id = target.closest('.list-group-item').data('form-id');

        $('.form-doc-types').hide();
        $(`#${id}`).show();
    });

    // TODO: показать данные АП
    $(document).on('click', '#confirm-ap', function(event) {
        event.preventDefault();
        $('#selected-ap').show();
        $('#btn-choose-ap').hide();
    });

    // TODO: таблицы заявок в АЦ
    $(document).on('click', '#open-tableCustomersRequest', function(event) {
        event.preventDefault();
        $('#table-customersRequest').show('fade');
        $('#table-recordInWork').hide();
        $('#table-personal-people').hide();
        $('#table-preparedReports').hide();
        $('#table-sentReports').hide();
    });
    $(document).on('click', '#open-tableRecordInWork', function(event) {
        event.preventDefault();
        $('#table-recordInWork').show('fade');
        $('#table-customersRequest').hide();
        $('#table-personal-people').hide();
        $('#table-preparedReports').hide();
        $('#table-sentReports').hide();
    });
    $(document).on('click', '#open-tablePreparedReports', function(event) {
        event.preventDefault();
        $('#table-preparedReports').show('fade');
        $('#table-customersRequest').hide();
        $('#table-personal-people').hide();
        $('#table-recordInWork').hide();
        $('#table-sentReports').hide();
    });
    $(document).on('click', '#open-tableSentReports', function(event) {
        event.preventDefault();
        $('#table-sentReports').show('fade');
        $('#table-customersRequest').hide();
        $('#table-personal-people').hide();
        $('#table-preparedReports').hide();
        $('#table-recordInWork').hide();
    });

    // Сроки проведения аттестации
    // $('.popper').popover({
    //  container: 'body',
    //  placement: 'top',
    //  trigger: 'hover',
    //  html: true,
    //  content: function() {
    //      return $(this).next('.popper-content').html();
    //  }
    // });

    // Сведения об организации
    $(document).on('click', '#btnSearchConfirm', function(event) {
        event.preventDefault();
        $('#infoUl').show('fade');
        $('#btnAddInfo').hide();
    })

    // Активные заголовки в аккордеоне
    $(document).on('click', '.card-header', function(event) {
        event.preventDefault();
        $(".card-header").removeClass('active');
        $(this).addClass('active');
    });

    // $(document).on('click', '.static-text-sublevel a[data-toggle="collapse"]', function (event) {
    //  event.preventDefault();
    //  $('.static-text-sublevel a[data-toggle="collapse"]').removeClass('active');
    //  $(this).addClass('active');
    // });

    // Просмотр по людям/записям
    $(document).on('click', '#view-people', function(event) {
        event.preventDefault();
        $('#table-personal-people').show('fade');
        $('#table-customersRequest').hide();
        $('#table-recordInWork').hide();

        $('#table-preparedReports').hide();
        $('#table-sentReports').hide();
    })
    $(document).on('click', '#view-records', function(event) {
        event.preventDefault();
        $('#table-customersRequest').show('fade');
        $('#table-personal-people').hide();
        $('#table-recordInWork').hide();

        $('#table-preparedReports').hide();
        $('#table-sentReports').hide();
    })

    // Скрыть/показать левую панель в документах
    $(document).on('click', '#minimizePanel', function(event) {
        event.preventDefault();
        $("#leftMenuPersonal").hide();
        $(this).hide();
        $('#openPanel').show();
        $("#rightTablePersonal").removeClass('col-lg-8 col-xl-9');
    });
    $(document).on('click', '#openPanel', function(event) {
        event.preventDefault();
        $("#leftMenuPersonal").show();
        $('#minimizePanel').show();
        $(this).hide();
        $("#rightTablePersonal").addClass('col-lg-8 col-xl-9');
    });

});

// left menu in centers-list
// $(window).scroll(function() {
//     let topPosLeft = $(document).scrollTop();
//     if (topPosLeft > 0) {
//         $('.left-main').addClass('fixed-left-main');
//     } else {
//         $('.left-main').removeClass('fixed-left-main');
//     }
// })

//
$('#btnEditInfo').click(function() {
    $('#orgInfoEdit').show('fade');
    $('#infoEdit').hide();
});
$('#cancelInfoEdit').click(function() {
    $('#orgInfoEdit').hide();
    $('#infoEdit').show('fade');
});

// $('#membershipSelection').change(function() {
//     if ($(this).val() == 'one') {
//         $('#membershipYes').hide();
//         $('#membershipNo').hide();
//     } else if ($(this).val() == 'two') {
//         $('#membershipYes').show();
//         $('#membershipNo').hide();
//     } else {
//         $('#membershipYes').show();
//         $('#membershipNo').show();
//     }
// })

$('#membershipSelection').change(function() {
    if ($(this).prop('checked')) {
        $('#membershipYes').toggle();
    } else {
        $('#membershipYes').hide();
    }
})