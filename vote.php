
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="./favicon.ico">

    <title>Jumbotron Template for Bootstrap</title>

    <!-- Bootstrap core CSS -->
    <link href="./css/bootstrap.cerulean.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="./css/jumbotron.css" rel="stylesheet">

    <!-- Just for debugging purposes. Don't actually copy these 2 lines! -->
    <!--[if lt IE 9]><script src="./assets/js/ie8-responsive-file-warning.js"></script><![endif]-->
    <script src="./js/ie-emulation-modes-warning.js"></script>

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>

    <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">Spiffomatic64's Twitch Stuff</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
          <form class="navbar-form navbar-right" role="form">
            <div class="form-group">
              <input type="text" placeholder="Username" class="form-control">
            </div>
            <div class="form-group">
              <input type="password" placeholder="Password" class="form-control">
            </div>
            <button type="submit" class="btn btn-success">Sign in</button>
          </form>
        </div><!--/.navbar-collapse -->
      </div>
    </nav>

    <!-- Main jumbotron for a primary marketing message or call to action -->
    <div class="jumbotron">
      <div class="container">
        <h1>Hi Friends!</h1>
        <p>This will be the home for any/all twitch replaced stuffs. (Including the future "Control Panel"). Right now its a work in progress, check back later!</p>
        <p><a class="btn btn-primary btn-lg" href="#" role="button">Learn more &raquo;</a></p>
      </div>
    </div>

    <div class="container">
      <!-- Example row of columns -->
      <div class="row">
        <div class="col-md-6">
          <h2>Scary Features Poll</h2>       
            <div id="scary" lass="btn-group-vertical" data-toggle="buttons">
            </div>
        </div>
        <div class="col-md-6">
          <h2>Interactive Features Poll</h2>
            <div id="interactive" lass="btn-group-vertical" data-toggle="buttons">
            </div>
        </div>
      </div>

      <hr>

      <footer>
        <p>&copy; twitch.tv/Spiffomatic64 2014</p>
      </footer>
    </div> <!-- /container -->


    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <script src="./js/bootstrap.min.js"></script>
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="./js/ie10-viewport-bug-workaround.js"></script>
    <script>
        $( document ).ready(function() {
            $('#scary').html('<div id="loader"><img src="css/loader.gif" alt="loading..."></div>');
            $('#interactive').html('<div id="loader"><img src="css/loader.gif" alt="loading..."></div>');
            
            var scaryuri  = 'https://api.github.com/repos/spiffomatic64/SpiffBot/issues?state=open&labels=enhancement,scary';
            var interactiveuri  = 'https://api.github.com/repos/spiffomatic64/SpiffBot/issues?state=open&labels=enhancement,interactive';
            var output = "";
            
            $.getJSON(scaryuri, function(json){
              issues = json;    
              outputPageContent('#scary',issues);
              
            }).done(function(){
                $.getJSON(interactiveuri, function(json){
                  issues = json;    
                  outputPageContent('#interactive',issues);
                });
              });
            
            $.getJSON(interactiveuri, function(json){
              issues = json;    
              output = "";
              outputPageContent('#interactive',issues);
            });
            
            
            function outputPageContent(put,data) {
                $.each(data, function(index) {
                    output = output + '<label class="btn btn-default" data-toggle="tooltip" data-placement="right" title="'+data[index].body+'">';
                    output = output + '<input type="radio" name="options" id="option1" autocomplete="off">'+data[index].title;
                    output = output + '</label> ';
                });
                $(put).html(output);
                $('[data-toggle="tooltip"]').tooltip()
            }
        });
       
    </script>
  </body>
</html>
