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
      if (rnd < acc) {
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
      $('#current-info').html(info.trackName + '<br /> by ' + info.artistName);
      $('audio')[0].volume = 0.25;
    },
    get_new_song: function(genre, callback) {
      var _that = this;
      var url = '/api/random';
      if (genre) {
        url += '?genre=' + genre;
      }
      $.get(url, function(data) {
        _that.update_info(data);
        if (callback)
          callback();
      });
    },
    like: function() {
      genres[this.info.genre] *= 2;
      liked.push(this.info.artistName);
      var _that = this;
      this.get_new_song(weighted_average(genres), function() {
        _that.play();
      });
      this.play();
    },
    dislike: function() {
      genres[this.info.genre] /= 2;
      var _that = this;
      this.get_new_song(weighted_average(genres), function() {
        _that.play();
      });
    },
  };

  async.parallel({
    // get genre list
    genre: function(callback) {
      $.get('/api/genres', function(data) {
        _.each(data, function(genre_id) {
          genres[genre_id] = 4;
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

  $('#start-page').click(function() {
    $(this).hide();
    var start_page = $(this);
    song.play();
    var count_from = 45;
    var countdown = new Countdown(count_from, function(seconds) {
      console.log(Math.floor((seconds/count_from) * 100) + '%');
      $('#progress-bar').css('width', Math.floor((seconds/count_from) * 100) + '%')
    }, function() {
      start_page.find('#start h1').text('Please wait...');
      start_page.show();
      window.open('/recommend?artists=' + encodeURIComponent(liked.join(';')), "_self");
    });
  });
})(jQuery);
