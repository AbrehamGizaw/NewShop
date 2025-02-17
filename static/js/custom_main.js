    // Readme : This file contains basic js scripts of our own just like main.js, but custom
    
    // if we are in login page, show only registration popup
    var path = window.location.pathname;
    // if(path.includes("accounts/login/") )
    // {
    //     document.getElementById('id_modal_div').className = "modal-dialog modal-lg"; //widen the modal 
    //     document.getElementById('id_signin_popuper').remove(); //remove sign in tab btn
    //     document.getElementById('tab-signin').remove(); //remove sign in content
    //     document.getElementById('tab-register').className = "tab-pane fade active show" //show register content
    //     let reg_tab = document.getElementById('id_register_popuper');
    //     reg_tab.querySelector("a").className = "tab-link active";
        
    // }

    // change Tab width for sign in and signup
    // $(".tab-link").click(function () {
    //     var link = (this.href).toString().split("#")[1];
    //     var modal_div = $("#id_modal_div")
    //     if (link == 'tab-signin') { modal_div.removeClass("modal-lg").addClass("modal-md") }

    //     else { modal_div.removeClass("modal-md").addClass("modal-lg") }

    // });

    // password view/ hide functionality
    function show_hide_pw(ele){
        let viewer = $(ele);
        let pw_field = ele.parentElement.querySelector(".form-control")
        if (pw_field.type == "password"){
            pw_field.type='text'; 
            viewer.removeClass("fi-rr-eye-crossed") //change icon
                .addClass("fi-rr-eye") 
                .attr("title","Hide Password") //change title
            }
        
        else{
            pw_field.type='password'; 
            viewer.removeClass("fi-rr-eye")
                .addClass("fi-rr-eye-crossed")
                .attr("title","Show Password");
            }
    }

    // if on signup, always display main captcha, check if popup should use 
    // else check if popup should use
    // function deciding if the recaptcha on popup login form should be used or not based on user attempt
    function captcha_activator(include_captcha_on_load="false", view_captcha=false, ){
        var captcha_elem = document.getElementById('id_captcha')
            
        if(captcha_elem){ 
            if (include_captcha_on_load == "true" || view_captcha ){ // if captcha on popup login form should be included 
                // view_captcha comes from each response, and include_captcha is loaded when template is rendered at first
                captcha_elem.style['display'] = "block";
                captcha_elem.setAttribute("required",true);
                
                if(view_captcha) {grecaptcha.reset();}
            }

            else{ // if captcha should not be displayed
                captcha_elem.style['display'] = "none";
                captcha_elem.setAttribute("required",false)
            }
        
        }
    }


    // function for popup login form
    function popup_login_form_submit(csrf_token, include_captcha_on_load="false"){
        var email = document.getElementById('id_email').value;
        var password = document.getElementById("id_password").value;
        var form_data = { 'csrfmiddlewaretoken': csrf_token, 
                          'email': email, 'password': password,
                          'g-recaptcha-response': $('#g-recaptcha-response').val()
                        }
        
        if (document.getElementById('id_remember').checked){
          form_data['remember'] = true;
        }
        
        $.ajax({
          type: "post", dataType: "json",
          url: "/accounts/login/",
          data: form_data,
          success: function (response) {
            if (response['logged_in'] == true) {
                window.location.assign(response['redirect']); 
            }
            
            else { 
              document.getElementById("id_main_form").innerHTML=response['html'];
              captcha_activator(include_captcha_on_load = include_captcha_on_load, view_captcha = response['view_captcha']);
            }
  
          },
  
          error: (response) => {
            var status_code = response['status']; 
  
            // if locked
            if (status_code == 429){window.location.assign("/accounts/locked/")}
            
            // if server error
            else if(status_code == 500){alert("Looks like we got some error on our end. Please try again later!")}
            
            else{
                alert("An error occurred! Please try again late."); 
                console.log(response);
            }
  
          }
  
        });
  
  
        return false;

    }

    