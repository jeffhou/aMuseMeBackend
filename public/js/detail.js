(function($) {
  var songs = $('.song');
  _.each(songs, function(song) {
    var audio = $(song).find('audio')[0];
    audio.volume = 0.25;
    $(song).click(function() {
      if (audio.paused) {
        audio.play();
      } else {
        audio.pause();
      }
    });
  });
})(jQuery);
