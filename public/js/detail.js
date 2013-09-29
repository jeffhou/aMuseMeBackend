(function($) {
  var songs = $('.song');
  _.each(songs, function(song) {
    var audio = $(song).find('audio')[0];
    console.log(song);
    console.log(audio);
    $(song).click(function() {
      console.log('playing');
      if (audio.paused) {
        audio.play();
      } else {
        audio.pause();
      }
    });
  });
})(jQuery);
