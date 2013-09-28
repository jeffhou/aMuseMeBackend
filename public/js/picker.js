(function($) {
  var genres = {};
  var song;
  var weighted_average = function(genres) {
    var totals = [];
    var running_total = 0;
    var genre_pairs = _.pairs(genres);

    _.each(genre_pairs, function(pair) {
      running_total += pair[1];
      totals.push(running_total);
    });
    var rnd = Math.floor(Math.random() * running_total);

    _.each(totals, function(total, i) {
      if (rnd < total) {
        return genre_pairs[i][0];
      }
    });
  };

  async.parallel({
    // get genre list
    genre: function(callback) {
      $.get('/api/genres', function(data) {
        _.each(data, function(genre_id) {
          genres[genre_id] = 8;
        });
        callback(null);
      });
    },
    // get first random song
    random_song: function(callback) {
      $.get('/api/random', function(data) {
        callback(null, data);
      });
    }
  },
  function (err, res) {
    song = res.random_song;
    var audio_elem = $('audio')
    audio_elem.attr('src', song.previewUrl);
    audio_elem[0].play();
  });
})(jQuery);
