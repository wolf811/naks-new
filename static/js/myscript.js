//Включение всплывающих подсказок
$(function() {
    $('[data-toggle="popover"]').popover();
})

$(function() {
    $('[data-toggle="tooltip"]').tooltip()
})

// Подчеркивание меню
$('.navbar-nav a').on("click", function() {
    $('.nav-link.active').removeClass('active');
    $(this).addClass('active');
});

$('.dropdown-menu a').on("click", function() {
    $('.dropdown-item.active').removeClass('active');
    $(this).addClass('active');
});

// Выделение кнопок показа подразделений
$('.show-units button').on("click", function() {
    $('.btn.active').removeClass('active');
    $(this).addClass('active');
});

// Кнопка - Наверх
$(document).ready(function() {
    $('body').append('<button class="top-arrow">');
    $('.top-arrow').click(function() {
        $('body').animate({ 'scrollTop': 0 }, 1000);
        $('html').animate({ 'scrollTop': 0 }, 1000);
    });
    $(window).scroll(function() {
        if ($(window).scrollTop() > 300) {
            $(".top-arrow").addClass("top-arrow-active");
        } else {
            $(".top-arrow").removeClass("top-arrow-active");
        }
    });
});

// Календарик
$(function() {
    $('div[name="datepicker"]').datetimepicker({
        locale: 'ru',
        format: 'DD.MM.YYYY',
        useCurrent: false,
        showClear: true,
        showClose: true,
        showTodayButton: true,
        icons: {
            previous: 'fa fa-chevron-left',
            next: 'fa fa-chevron-right',
            today: 'fa fa-bullseye',
            clear: 'fa fa-trash-o',
            close: 'fa fa-times',
        },
        tooltips: {
            today: 'Сегодня',
            clear: 'Очистить',
            close: 'Закрыть',
        },
    });
});

// Плавающее правое меню
if ($('.right-main').length > 0) {
    $(function() {
        var topPos = $('.right-main').offset().top;
        $(window).scroll(function() {

            var top = $(document).scrollTop(),
                pip = $('.footer').offset().top,
                height = $('.right-main').outerHeight();

            if (top > topPos && top < pip - height) {
                $('.right-main').addClass('fixed').removeAttr("style");
            } else if (top > pip - height) {
                $('.right-main').removeClass('fixed').css({ 'position': 'absolute', 'bottom': '0' });
            } else {
                $('.right-main').removeClass('fixed');
            }
        });
    });
}

// Показать еще
$('#btnNews_showMore').click(function() {
    $('#blockNews_02').slideDown();
});

$('#btnAgreement_showMore').click(function() {
    $('#blockPartners_02').slideDown();
});


// Остановка видео в модальном окне
var video = document.getElementById("myVideoPlayer");

function stopVideo() {
    video.pause();
    video.currentTime = 0;
}

// Авторизация/Регистрация
$('#for-registration').click(function() {
    $('#registration-page').fadeIn('slow');
    $('#login-page').hide();
});

$('#to-authorization').click(function() {
    $('#login-page').fadeIn('slow');
    $('#registration-page').hide();
});

$('#save-reg').click(function() {
    $('#reg-info').fadeIn('slow').delay(1000);
    $('#reg-fields').hide();
});

$('#close-reg-info').click(function() {
    $('#login-page').fadeIn('slow');
    $('#registration-page').hide();
    return (false);
});

$('#to-recovery').click(function() {
    $('#pass-recovery').fadeIn('slow');
    $('#login-page').hide();
});

// Авторизация/Регистрация - для заявок
// $('#for-registration').click(function() {
//  $('#registration-appl').fadeIn('slow');
//  $('#login-page').hide();
// });

// $('#to-authorization').click(function() {
//  $('#login-page').fadeIn('slow');
//  $('#registration-page').hide();
// });

$('#save-reg-appl').click(function() {
    $('#reg-info-appl').fadeIn('slow').delay(1000);
    $('#reg-fields-appl').hide();
});

$('#close-reg-info').click(function() {
    $('#login-page').fadeIn('slow');
    $('#registration-page').hide();
    return (false);
});

$('#to-recovery').click(function() {
    $('#pass-recovery').fadeIn('slow');
    $('#login-page').hide();
});

// jQuery(document).ready(function($) {
//  var url=document.location.href;
//  $.each($("#menu a"),function(){
//      if(this.href==url){
//          $(this).addClass('active');
//      }
//  });
// });

// Изменение текста при меньшем разрешении экрана
$(document).ready(function() {
    $(window).resize(function() {
        var windowWidth = $(window).width();
        if (windowWidth > 768) {
            $('.btn-outline-dark[name="btnOpenDoc"]').html('<i class="fa fa-file-pdf-o mr-2"></i>Открыть документ');
        } else {
            $('.btn-outline-dark[name="btnOpenDoc"]').html('<i class="fa fa-file-pdf-o mr-2"></i>Открыть');
        }
    });
});
// END


// $(document).ready(function() {
//     $("nav > ul > li").mouseover(function() {
//         var the_width = $(this).find("a").width();
//         var child_width = $(this).find("ul").width();
//         var width = parseInt((child_width - the_width)/2);
//         $(this).find("ul").css('left', -width);
//     });
// });


//     var data = {
//      'modal-title': 'Форум «Территория NDT»',
//      'modal-text': 'Ежегодный Форум «Территория NDT» является ведущей профессиональной \
//      площадкой для конструктивного диалога заинтересованных сторон и демонстрации новейших \
//      достижений и разработок. Крупнейшая специализированная выставка оборудования и технологий \
//      неразрушающего контроля и технической диагностики ежегодно объединяет более 100 компаний – \
//      разработчиков и поставщиков российских и зарубежных брендов, сервисные учебные и сертификационные \
//      центры, ВУЗы, НИИ, специализированные издания.',
//      'modal-photos': ['/static/images/NDT-0617.jpg', '/static/images/NDT-0427.jpg', '/static/images/IMG_7428.JPG']

//     };

// function insertToModal (data) {
//  $('.modal-title').html(data['modal-title']);
//  $('.modal-text').html(data['modal-text']);
//  for(var element of data['modal-photos']) {
//      $($('.carousel-inner > .carousel-item')[data['modal-photos'].indexOf(element)]).attr('src', element);
//  }
// }

// insertToModal(data);

$(document).ready(function() {
    // Фильтр квалификаций в зависимости от стандрта
    $('#filter-ps').change(function() {
        var val = $(this).val();
        if (val == 'ps-01') {
            $('#filter-kval option[data-name="welder"]').show();
            $('#filter-kval option[data-name="operator"]').hide();
            $('#filter-kval option[data-name="rezchik"]').hide();
            $('#filter-kval option[data-name="controler"]').hide();
        } else if (val == 'ps-02') {
            $('#filter-kval option[data-name="operator"]').show();
            $('#filter-kval option[data-name="welder"]').hide();
            $('#filter-kval option[data-name="rezchik"]').hide();
            $('#filter-kval option[data-name="controler"]').hide();
        } else if (val == 'ps-03') {
            $('#filter-kval option[data-name="rezchik"]').show();
            $('#filter-kval option[data-name="welder"]').hide();
            $('#filter-kval option[data-name="operator"]').hide();
            $('#filter-kval option[data-name="controler"]').hide();
        } else if (val == 'ps-04') {
            $('#filter-kval option[data-name="controler"]').show();
            $('#filter-kval option[data-name="welder"]').hide();
            $('#filter-kval option[data-name="operator"]').hide();
            $('#filter-kval option[data-name="rezchik"]').hide();
        } else if (val == 'ps-00') {
            $('#filter-kval option[data-name="welder"]').show();
            $('#filter-kval option[data-name="operator"]').show();
            $('#filter-kval option[data-name="rezchik"]').show();
            $('#filter-kval option[data-name="controler"]').show();
        }
    });
});

// Правка цвета таблиц реестра АЦ
$(window).resize(function() {
    if ($(window).width() <= 1199) {
        let rowActingAc = $('#tableActingAc_01 tr').length;
        let rowPausedAc = $('#tablePausedAc_01 tr').length;
        let rowExcludedAc = $('#tableExcludedAc_01 tr').length;

        if (rowActingAc % 2 != 0) {
            $('#tableActingAc_02').removeClass('table-striped');
            $('#tableActingAc_02').addClass('table-striped-even');
        };

        if (rowPausedAc % 2 != 0) {
            $('#tablePausedAc_02').removeClass('table-striped');
            $('#tablePausedAc_02').addClass('table-striped-even');
        };

        if (rowExcludedAc % 2 != 0) {
            $('#tableExcludedAc_02').removeClass('table-striped');
            $('#tableExcludedAc_02').addClass('table-striped-even');
        };

    } else {
        $('#tableActingAc_02, #tablePausedAc_02, #tableExcludedAc_02').addClass('table-striped');
        $('#tableActingAc_02, #tablePausedAc_02, #tableExcludedAc_02').removeClass('table-striped-even');
    }

});


// Выбранные параметры поиска по реестру АЦ, на главной карте
$('#btnSaveFilterAc').click(function() {
    $('#btnFilterAc').hide();
    $('#selectedOptions').show();
})

// $('#btnSaveFilterIndex').click(function() {
//     $('#btnFilterIndex').hide();
//     $('#btnFilterResultIndex').show();
// })

$('#btnSubscription').click(function() {
    $('.subscription').hide();
    setTimeout(function() {
        $('.subscription').show();
    }, 1500);
    $('.result-subscription').show();
    setTimeout(function() {
        $('.result-subscription').hide();
    }, 1500);
    return false;
})


// $('#loginBtn_02').click(function() {
//     $('#btnGroupEntered').show();
//     $('#loginBtn_01').hide();
// });
// $('#exitBtn').click(function() {
//     $('#btnGroupEntered').hide();
//     $('#loginBtn_01').show();
// });

// Vue.use(Vuex)

const store = new Vuex.Store({
    state: {
        authUser: {},
        isAuthenticated: false,
        jwt: localStorage.getItem('token'),
      endpoints: {
        // obtainJWT: '/api-token-auth/',
        // refreshJWT: '/api-token-refresh/',
        // verifyJWT:  '/api-token-verify/'
        obtainJWT: '/api-token-auth/',
        refreshJWT: '/api-token-refresh/',
        baseUrl: '/'
      }
    },
    mutations: {
        setAuthUser(state, {
          authUser,
          isAuthenticated
        }) {
          Vue.set(state, 'authUser', authUser)
          Vue.set(state, 'isAuthenticated', isAuthenticated)
        },
        updateToken(state, newToken) {
          // TODO: For security purposes, take localStorage out of the project.
          localStorage.setItem('token', newToken);
          state.jwt = newToken;
        },
        removeToken(state) {
          // TODO: For security purposes, take localStorage out of the project.
          localStorage.removeItem('token');
          state.jwt = null;
        }
      }
})


if ($('#auth_app').length > 0) {
    var vm_auth = new Vue({
        delimiters: ['[[', ']]'],
        el: '#auth_app',
        data() {
            return {
                title: 'auth_app',
                logged_in: true,
                username: '',
                password: '',
                endpoints: {
                    // path('api-token-auth/', obtain_jwt_token),
                    // path('api-token-refresh/', refresh_jwt_token),
                    // path('api-token-verify/', verify_jwt_token),
                    obtainJWT: '/api-token-auth/',
                    refreshJWT: '/api-token-refresh/',
                    verifyJWT:  '/api-token-verify/'
                }
            }
        },
        beforeMount() {
            this.jwt = localStorage.getItem('jwtToken')
            // if ((this.jwt).length == 0) {
            //     localStorage.setItem('token', newToken)
            // }
        },
        methods: {
            authenticate: function() {
                const payload = {
                    email: this.username,
                    password: this.password
                }
                const base = {
                    baseURL: this.$store.state.endpoints.baseUrl,
                    headers: {
                    // Set your Authorization to 'JWT', not Bearer!!!
                      Authorization: `JWT ${this.$store.state.jwt}`,
                      'Content-Type': 'application/json'
                    },
                    xhrFields: {
                        withCredentials: true
                    }
                }
                axios
                    .post(this.$store.state.endpoints.obtainJWT, payload)
                    .then(response => {
                        // localStorage.setItem('token', newToken);
                        this.$store.commit('updateToken', response.data.token)
                        // const newToken = response.data.token;
                        localStorage.setItem('token', newToken);
                    })
                    .finally()
            },
            logout_current_user: function() {
                // var data = {
                //     logout_current_user: true,
                // }
                let formData = new FormData();
                formData.append('logout_current_user', true);
                axios
                .post('/users/logout/', formData)
                .then(response => {
                    console.log('response', response.data);
                    this.logged_in = false;
                })
                .finally(() => {
                    // this.$cookies.set("sro_members_updated", "1", "1h");
                    console.log('finally logout callback');
                })
            }
        }
    });
}

