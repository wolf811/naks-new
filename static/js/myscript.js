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
        $('body').animate({
            'scrollTop': 0
        }, 1000);
        $('html').animate({
            'scrollTop': 0
        }, 1000);
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
                $('.right-main').removeClass('fixed').css({
                    'position': 'absolute',
                    'bottom': '0'
                });
            } else {
                $('.right-main').removeClass('fixed');
            }
        });
    });
}

// $(window).resize(function() {
//     if ($(window).width() > 768) {

//     }
// });


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
// $('#for-registration').click(function() {
//     $('#registration-page').fadeIn('slow');
//     $('#login-page').hide();
// });

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

// Подтверждение подписки на рассылку
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

// Подтверждение восстановления пароля
// $('#btnSavePassRecovery').click(function() {
//     $('.pass-is-valid').show('fade');
//     return false;
// })


// $('#loginBtn_02').click(function() {
//     $('#btnGroupEntered').show();
//     $('#loginBtn_01').hide();
// });
// $('#exitBtn').click(function() {
//     $('#btnGroupEntered').hide();
//     $('#loginBtn_01').show();
// });

// Vue.use(Vuex)

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

if ($('#auth_app').length > 0) {
    var vm_auth = new Vue({
        delimiters: ['[[', ']]'],
        el: '#auth_app',
        data() {
            return {
                title: 'auth_app',
                logged_in: false,
                registered: false,
                username: '',
                password: '',
                token: '',
                edo_token: '',
                edo_token_created: null,
                urStatus: 'UL',
                endpoints: {
                    // path('api-token-auth/', obtain_jwt_token),
                    // path('api-token-refresh/', refresh_jwt_token),
                    // path('api-token-verify/', verify_jwt_token),
                    loginRequest: '/users/login/',
                    obtainToken: '/api-token-auth/',
                    registerNew: '/users/register/',
                    recoverPassword: '/users/recover-password/',
                    saveNewPassword: '/users/update-password/',
                    refreshToken: '/users/refresh-edo-token/',
                    authEdoByToken: 'https://ac.naks.ru/auth/external/auth.php'
                    // refreshJWT: '/api-token-refresh/',
                    // verifyJWT:  '/api-token-verify/'
                },
                form_errors: {
                    email: {
                        message: ''
                    },
                    password: {
                        message: ''
                    }
                },
                recoverRequestMessageSuccess: null,
                recoverRequestMessageFailure: null,
                passwordRecoverUrl: null,
                stupidpot: null,
                showSpinner: false,
            }
        },
        created: function() {
            axios.interceptors.response.use(undefined, function(err) {
                return new Promise(function(resolve, reject) {
                    if (err.status === 401 && err.config && !err.config.__isRetryRequest) {
                        // if you ever get an unauthorized, logout the user
                        //   this.$store.dispatch(AUTH_LOGOUT)
                        console.log(resolve, reject);
                        this.logged_in = false;
                        // you can also redirect to /login if needed !
                    }
                    throw err;
                });
            });
        },
        beforeMount() {
            this.token = localStorage.getItem('token');
            this.user = localStorage.getItem('user');
            if (this.token && this.user) {
                this.logged_in = true;
                axios.defaults.headers.common['Authorization'] = `Token ${this.token}`;
            }
            try {
                let edoToken = localStorage.getItem('edo_token');
                if (edoToken) {
                    edoToken = JSON.parse(edoToken);
                    this.edo_token = edoToken.token;
                    this.edo_token_created = edoToken.created;
                }
            } catch (e) {
                console.log(e);
                //pass
            }
        },
        methods: {
            //TODO: сделать визуализации сложности пароля:
            //красная линия - пароль слишком простой и т.д.
            test: function() {
                console.log('callback');
            },
            cleanLocalStorage: function() {
                localStorage.removeItem('token');
                localStorage.removeItem('user');
                this.logged_in = false;
            },
            resetForm: function() {
                this.form_errors = {
                    email: {
                        message: ''
                    },
                    password: {
                        message: ''
                    }
                }
            },
            toggle_login_panel: function() {
                this.resetForm();
                $("#registration-page").hide();
                $("#pass-recovery").hide();
                $("#login-page").fadeIn('slow');
            },
            toggle_recovery_panel: function() {
                this.recoverRequestMessageFailure = null;
                this.recoverRequestMessageSuccess = null;
                $("#login-page").hide();
                $("#pass-recovery").fadeIn('slow');
            },
            loginFormSend: function(e) {
                if (e.keyCode === 13) {
                    this.authenticate();
                }
            },
            authenticate: function() {
                console.log('pressed login');
                if (this.logged_in == true) {
                    $('#modal-authorization').modal('hide');
                    return
                }
                const payload = {
                    email: this.username,
                    password: this.password
                }
                axios
                    .post(this.endpoints.loginRequest, payload)
                    .then(response => {
                        // localStorage.setItem('token', newToken);
                        console.log('RESPONSE', response, response.status);
                        if (!response.data['errors']) {
                            this.form_errors.email.message = '';
                            this.form_errors.password.message = '';
                            const token = response.data.token;
                            localStorage.setItem('token', token);
                            localStorage.setItem('user', this.username);
                            let edoToken = { 'token': response.data.edo_token, 'created': response.data.edo_token_created };
                            localStorage.edo_token = JSON.stringify(edoToken);
                            this.edo_token = response.data.edo_token;
                            this.edo_token_created = response.data.edo_token_created;
                            this.logged_in = true;
                            this.user = this.username;
                            $('#modal-authorization').modal('hide');
                        } else {
                            let errors = response.data['errors'];
                            this.form_errors.email.message = errors;
                            this.form_errors.password.message = errors;
                            console.log('errors', errors);
                        }
                    })
                    .finally(() => {
                        console.log('authenticated finally callback');
                    })
            },
            toggle_register_pannel: function() {
                this.resetForm();
                $('#registration-page').fadeIn('slow');
                $('#login-page').hide();
            },
            register_user: function() {
                if (this.logged_in == true) {
                    $('#modal-authorization').modal('hide');
                    return
                }
                this.registered = false;
                this.showSpinner = true;
                this.resetForm();
                // this.resetForm();
                let payload = {
                    'email': this.username,
                    'password': this.password,
                    'ur_status': this.urStatus
                }
                if (this.stupidpot) {
                    payload['honeypot'] = this.stupidpot
                }
                axios
                    .post(this.endpoints.registerNew, payload)
                    .then(response => {
                        console.log('register response', response);
                        if (response.data['form_errors']) {
                            this.showSpinner = false;
                            for (var err of response.data['form_errors']) {
                                if (err.field === "email") {
                                    this.form_errors.email.message = err.errors.join("<br>");
                                }
                                if (err.field.includes("password")) {
                                    this.form_errors.password.message = err.errors.join("<br>");
                                }
                            }
                        } else {
                            this.registered = true;
                            this.logged_in = true;
                            this.token = response.data.token;
                            this.user = this.username;
                            localStorage.setItem('token', this.token);
                            localStorage.setItem('user', this.username);
                            let edoToken = { 'token': response.data.edo_token, 'created': response.data.edo_token_created };
                            localStorage.edo_token = JSON.stringify(edoToken);
                            this.edo_token = edoToken.token;
                            this.edo_token_created = edoToken.created;
                            this.showSpinner = false;
                        }
                    })
                    .catch(error => {
                        console.log('CATCHED ERROR', error)
                    })
                    .finally(console.log('finnaly register ok'))
            },
            logout_current_user: function() {
                // var data = {
                //     logout_current_user: true,
                // }
                console.log('logging out...');
                let formData = new FormData();
                formData.append('logout_current_user', true);
                axios
                    .post('/users/logout/', formData)
                    .then(response => {
                        console.log('response', response.data);
                        if (response.data['user_logged_out']) {
                            this.logged_in = false;
                        }
                    })
                    .finally(() => {
                        this.username = '';
                        this.password = '';
                        this.user = '';
                        this.logged_in = false;
                        this.registered = false;
                        localStorage.clear();
                        // TODO: send REST request to logout on ac.naks.ru
                    })
            },
            send_recovery_email: function() {
                console.log('ajax call email sending with link to change password');
                this.recoverRequestMessageSuccess = null;
                this.recoverRequestMessageFailure = null;
                this.showSpinner = true;
                data = { "email": this.username }
                axios
                    .post(this.endpoints.recoverPassword, data)
                    .then(response => {
                        console.log('RECOVER RESPONSE', response);
                        if (response.data['password_recovery_email_sent']) {
                            this.recoverRequestMessageSuccess = response.data['password_recovery_email_sent'];
                        }
                        if (response.data['password_recovery_error']) {
                            this.recoverRequestMessageFailure = response.data['password_recovery_error'];
                        }
                        if (response.data['user_recover_link']) {
                            this.passwordRecoverUrl = response.data['user_recover_link']
                        }
                    })
                    .catch(err => console.log('recover email ERROR', err))
                    .finally(() => {
                        this.showSpinner = false;
                        console.log('send request complete finally callback');
                    })
            },
            refresh_edo_token: function() {
                axios
                    .post(this.endpoints.refreshToken)
                    .then(response => {
                        console.log('RESPONSE', response);
                        this.edo_token = response.data.edo_token;
                        this.edo_token_created = response.data.edo_token_created;
                        // var existing = localStorage.getItem('edo_token');
                        let edoToken = { 'token': this.edo_token, 'created': this.edo_token_created };
                        localStorage.edo_token = JSON.stringify(edoToken);
                    })
                    .catch(error => { console.log('ERROR', error); })
                    .finally(() => { console.log('REFRESHING TOKEN'); })
            },
            edo_login_by_token: function() {
                var token_created = new Date(this.edo_token_created);
                var oneHourBefore = new Date();
                oneHourBefore.setHours(oneHourBefore.getHours() - 1);
                // console.log(token_created, oneHourBefore);
                if (token_created < oneHourBefore) {
                    this.refresh_edo_token();
                }

                const edo_token = this.edo_token;
                const auth_url = this.endpoints.authEdoByToken;
                const edo_auth_url = `${auth_url}?token=${edo_token}`;
                // console.log('EDO AUTH TOKEN URL', edo_auth_url);
                if (edo_token.length > 0) {
                    window.location.href = edo_auth_url;
                } else {
                    console.log('ERROR: NO EDO TOKEN!');
                    return
                }

                // var form = document.createElement('form');
                // var data = document.createElement('input');
                // data.type="hidden";
                // data.name="auth";
                // data.value=`${this.edo_token}`;
                // form.method = 'post';
                // form.action = 'https://ac.naks.ru/auth/'
                // form.appendChild(data);
                // document.body.appendChild(form);
                // form.submit();
            }
        }
    });
}

if ($('#password_change_app').length > 0) {
    var vm_password_change = new Vue({
        delimiters: ['[[', ']]'],
        el: '#password_change_app',
        data() {
            return {
                // uid: this.$refs.uid.dataset.uid,
                // token: this.$refs.token.dataset.token,
                newPassword: '',
                newPasswordConfirm: '',
                serverConfirm: false,
                serverMessage: '',
                formErrors: null,
                endpoints: {
                    saveNewPassword: '/users/update-password/'
                },
            }
        },
        watch: {
            // :newVal, oldVal
            newPassword: function() {
                this.formErrors = null;
            },
            newPasswordConfirm: function() {
                this.formErrors = null;
            }
        },
        mounted() {
            this.uid = this.$refs.uid.dataset.uid;
            this.token = this.$refs.token.dataset.token;
        },
        methods: {
            saveNewPassword: function() {
                console.log('save button pressed');
                const newPassword1 = this.newPassword;
                const newPassword2 = this.newPasswordConfirm;
                const uid = this.uid;
                const token = this.token;
                let data = new FormData();
                data.append('new_password1', newPassword1);
                data.append('new_password2', newPassword2);
                axios
                    .post(`${this.endpoints.saveNewPassword}${uid}/${token}`, data)
                    .then(response => {
                        console.log('RESPONSE', response.data, typeof response.data['form_errors']);
                        if (response.data['password_updated']) {
                            this.serverConfirm = true;
                        }
                        if (response.data['form_errors']) {
                            this.formErrors = response.data['form_errors'][0];
                        }
                    })
                    .catch(err => { console.log('CHANGE PASSWORD ERROR') })
                    .finally(() => { console.log('server change finally callback') });
            }
        }
    })
}