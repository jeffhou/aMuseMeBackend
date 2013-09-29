(function($) {
  var genres = {};
  var liked = [];

  var weighted_average = function(genres, callback) {
    var running_total = 0, acc = 0;
    var genre_pairs = _.pairs(genres);

    _.each(genre_pairs, function(pair) {
      running_total += pair[1];
    });

    var rnd = Math.floor(Math.random() * running_total);

    for (var i=0; i < genre_pairs.length; i++) {
      acc += genre_pairs[i][1];
      console.log(rnd, acc, rnd<acc);
      if (rnd < acc) {
        console.log('less');
        return genre_pairs[i][0];
      }
    }
  };

  var song = {
    info: {},
    playing: false,
    pause: function() {
      $('audio')[0].pause();
      this.playing = false;
    },
    play: function() {
      $('audio')[0].play();
      this.playing = true;
    },
    toggle: function() {
      if (this.playing) {
        this.playing = false;
        this.pause();
      } else {
        this.playing = true;
        this.play();
      }
    },
    update_info: function(info) {
      var _that = this;
      this.info = info;
      // this doesn't work in chrome
      //$('audio').bind('ended', function() {
      ///  console.log('ended');
      ///  _that.get_new_song();
      ///});
      $('audio').attr('src', info.previewUrl);
      $('#current-art img').attr('src', info.artworkUrl100)
        .attr('width', 300);
      $('#current-info').html(info.trackName + '<br />' + info.artistName);
      $('audio')[0].volume = 0.25;
    },
    get_new_song: function(callback) {
      var _that = this;
      $.get('/api/random', function(data) {
        _that.update_info(data);
        _that.play();
        if (callback)
          callback();
      });
    },
    like: function() {
      genres[this.info.genre] *= 2;
      console.log(genres);
      liked.push(this.info.artistName);
      this.get_new_song();
    },
    dislike: function() {
      genres[this.info.genre] /= 2;
      console.log(genres);
      this.get_new_song();
    },
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
    song.update_info(res.random_song);
    song.play();
    $('#current-art').click(function() {
      song.toggle();
    });
    $('#thumbs-down').click(function() {
      song.dislike();
    });
    $('#thumbs-up').click(function() {
      song.like();
    });
  });
})(jQuery);
