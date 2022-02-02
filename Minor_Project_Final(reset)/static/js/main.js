// Scrolly.
  $('.scrolly').scrolly({
    offset: function() {
      return $header.height();
    }
  });
  $('.nav-link').on('click', function() {
  	$('.active').removeClass('active');
  	$(this).addClass('active');
  });
