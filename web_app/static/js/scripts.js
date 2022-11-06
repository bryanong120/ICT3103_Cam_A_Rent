// Signup form logic
$("form[name=signup_form").submit(function (e) {

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/signup",
        type: "POST",
        data: data,
        dataType: "json",
        success: function (resp) {
            window.location.href = "/user/verifyOTP";
        },
        error: function (resp) {
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});

//Login form logic
$("form[name=login_form").submit(function (e) {

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/login",
        type: "POST",
        data: data,
        dataType: "json",
        success: function (resp) {
			if (resp)
				window.location.href = "/user/loginOTP";
			else
				window.location.href = "/user/verifyOTP";
				
        },
        error: function (resp) {
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});

//Verify OTP form logic
$("form[name=verifyotp_form").submit(function (e) {

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/verifyOTP",
        type: "POST",
        data: data,
        dataType: "json",
        success: function (resp) {
            window.location.href = "/user/dashboard";
        },
        error: function (resp) {
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});

//Login OTP form logic
$("form[name=loginotp_form").submit(function (e) {

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/loginOTP",
        type: "POST",
        data: data,
        dataType: "json",
        success: function (resp) {
            window.location.href = "/user/dashboard";
        },
        error: function (resp) {
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});