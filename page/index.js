// Fade on scroll
// NOT CURRENTLY WORKING WITH FADE ON PAGE LOAD!!!

$(window).on("load",function() {
    $(window).scroll(function() {
      var windowBottom = $(this).scrollTop() + $(this).innerHeight();
      $(".fade").each(function() {
        /* Check the location of each desired element */
        var objectBottom = $(this).offset().top + $(this).outerHeight();
        
        /* If the element is completely within bounds of the window, fade it in */
        if (objectBottom < windowBottom) { //object comes into view (scrolling down)
          if ($(this).css("opacity")==0) {$(this).fadeTo(500,1);}
        } else { //object goes out of view (scrolling up)
          if ($(this).css("opacity")==1) {$(this).fadeTo(500,0);}
        }
      });
    }).scroll(); //invoke scroll-handler on page-load
  });


  $(document).ready(function(){
    hideAllTeamRoles();
    addHoverToRole();
    
  })


  function hideAllTeamRoles() {
    var names = ["davidPRole", "davidARole", "carterRole", "nickRole", "michaelRole"];
    names.forEach(role => {
      $(`#${role}`).hide();
    });
  }

  function toggleTeamRole(name, action) {
    if (action == "hide") {
      $(`#${name}`).hide();
    } else {
      $(`#${name}`).show();
    }
  }

  function addHoverToRole() {
    var names = ["davidP", "davidA", "carter", "nick", "michael"];
    names.forEach(name => {
      $(`#${name}Name`).hover(function(){
        toggleTeamRole(`${name}Role`, "show");
      }, function(){
        toggleTeamRole(`${name}Role`, "hide");
    });
    });
  }