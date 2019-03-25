//Включение всплывающих подсказок
$(function () {
	$('[data-toggle="popover"]').popover();
})

$(function () {
	$('[data-toggle="tooltip"]').tooltip()
})

// Подчеркивание меню
$('.navbar-nav a').on("click", function(){
	$('.nav-link.active').removeClass('active');
	$(this).addClass('active');
});

$('.dropdown-menu a').on("click", function(){
	$('.dropdown-item.active').removeClass('active');
	$(this).addClass('active');
});

// Выделение кнопок показа подразделений
$('.show-units button').on("click", function(){
	$('.btn.active').removeClass('active');
	$(this).addClass('active');
});

// Кнопка - Наверх
$(document).ready(function() {
	$('body').append('<button class="top-arrow">');
	$('.top-arrow').click(function() {
		$('body').animate({'scrollTop': 0}, 1000);
		$('html').animate({'scrollTop': 0}, 1000);
	});
	$(window).scroll(function(){
		if ($(window).scrollTop() > 300) {
			$(".top-arrow").addClass("top-arrow-active");
		}
		else {
			$(".top-arrow").removeClass("top-arrow-active");
		}
	});
});

// Календарик
$(function () {
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
$(function(){
	var topPos = $('.right-main').offset().top;
	$(window).scroll(function() { 

		var top = $(document).scrollTop(),
		pip = $('.footer').offset().top,
		height = $('.right-main').outerHeight();

		if (top > topPos && top < pip - height) {
			$('.right-main').addClass('fixed').removeAttr("style"); 
			// $('.footer').removeClass('mt-5');
		} else if (top > pip - height) {
			$('.right-main').removeClass('fixed').css({'position':'absolute','bottom':'0'}); 
			// $('.footer').removeClass('mt-5');
		} else {
			$('.right-main').removeClass('fixed'); 
			// $('.footer').addClass('mt-5');
		}
	});
});

// Показать еще
$('#btnNews_showMore').click(function() {
	$('#blockNews_02').slideDown();
});

$('#btnAgreement_showMore').click(function() {
	$('#blockPartners_02').slideDown();
});


// Остановка видео в модальном окне
var video = document.getElementById("myVideoPlayer");
function stopVideo(){
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
// 	$('#registration-appl').fadeIn('slow');
// 	$('#login-page').hide();
// });

// $('#to-authorization').click(function() {
// 	$('#login-page').fadeIn('slow');
// 	$('#registration-page').hide();
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
// 	var url=document.location.href;
// 	$.each($("#menu a"),function(){
// 		if(this.href==url){
// 			$(this).addClass('active');
// 		}
// 	});
// });

// Изменение текста при меньшем разрешении экрана
$(document).ready(function() {
	$(window).resize(function() {
		var windowWidth = $(window).width();
		if(windowWidth > 768) {
			$('.btn-outline-dark[name="btnOpenDoc"]').html('<i class="fa fa-file-pdf-o mr-2"></i>Открыть документ');
		}
		else {
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