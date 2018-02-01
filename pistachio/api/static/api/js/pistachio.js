// create module
var app = angular.module('pistachio', ['ngRoute', 'ngMaterial'])
    .run (function() {
        console.log('Pistachio is alive!')
    });
//configure for routing
// taratsang / -> template home.html and controller mainController
// taratsang /about -> template about.html and controller mainController
// taratsang /portfolio -> template portfolio.html and controller mainController
app.config(['$routeProvider', function($routeProvider) {
    $routeProvider
    //route for the home page
        .when('/', {
            templateUrl: '/static/api/pages/home.html',
            controller: 'mainController',
            title: 'HOME.'
        }).otherwise({
            redirectTo: '/'
        })
}]);

// =======================================
// Modal controller

app.controller('modalCtrl', function($scope,$mdDialog) {
    $scope.status = ' ';
    $scope.customFullscreen = false;


  //   $scope.showAddTrip = function(ev) {
  //   var confirm = $mdDialog.confirm()
  //           .cancel('X')
  //         .title('Would you like to delete your debt?')
  //         .textContent('All of the banks have agreed to forgive you your debts.')
  //         .ariaLabel('Lucky day')
  //         .targetEvent(ev)
  //         .ok('Please do it!');


  //   $mdDialog.show(confirm).then(function() {
  //     $scope.status = 'You decided to get rid of your debt.';
  //   }, function() {
  //     $scope.status = 'You decided to keep your debt.';
  //   });
  // };

   $scope.showAlert = function(ev) {
    // Appending dialog to document.body to cover sidenav in docs app
    // Modal dialogs should fully cover application
    // to prevent interaction outside of dialog
    $mdDialog.show(
      $mdDialog.alert()
        .parent(angular.element(document.querySelector('#popupContainer')))
        .clickOutsideToClose(true)
        .title('This is an alert title')
        .textContent('You can specify some description text in here.')
        .ariaLabel('Alert Dialog Demo')
        .ok('Got it!')
        .targetEvent(ev)
    );
  };

  $scope.showConfirm = function(ev) {
    // Appending dialog to document.body to cover sidenav in docs app
    var confirm = $mdDialog.confirm()
          .title('Would you like to delete your debt?')
          .textContent('All of the banks have agreed to forgive you your debts.')
          .ariaLabel('Lucky day')
          .targetEvent(ev)
          .ok('Please do it!')
          .cancel('Sounds like a scam');

    $mdDialog.show(confirm).then(function() {
      $scope.status = 'You decided to get rid of your debt.';
    }, function() {
      $scope.status = 'You decided to keep your debt.';
    });
  };

  $scope.showPrompt = function(ev) {
    // Appending dialog to document.body to cover sidenav in docs app
    var confirm = $mdDialog.prompt()
      .title('What would you name your dog?')
      .textContent('Bowser is a common name.')
      .placeholder('Dog name')
      .ariaLabel('Dog name')
      .initialValue('Buddy')
      .targetEvent(ev)
      .required(true)
      .ok('Okay!')
      .cancel('I\'m a cat person');

    $mdDialog.show(confirm).then(function(result) {
      $scope.status = 'You decided to name your dog ' + result + '.';
    }, function() {
      $scope.status = 'You didn\'t name your dog.';
    });
  };

  $scope.showAddTrip = function(ev) {
    $mdDialog.show({
      controller: DialogController,
      templateUrl: '/static/api/pages/addtrip_modal.html',
      parent: angular.element(document.body),
      targetEvent: ev,
      clickOutsideToClose:true,
      fullscreen: $scope.customFullscreen // Only for -xs, -sm breakpoints.
    })
    .then(function(answer) {
      $scope.status = 'You said the information was "' + answer + '".';
    }, function() {
      $scope.status = 'You cancelled the dialog.';
    });
  };

  $scope.showTabDialog = function(ev) {
    $mdDialog.show({
      controller: DialogController,
      templateUrl: 'tabDialog.tmpl.html',
      parent: angular.element(document.body),
      targetEvent: ev,
      clickOutsideToClose:true
    })
        .then(function(answer) {
          $scope.status = 'You said the information was "' + answer + '".';
        }, function() {
          $scope.status = 'You cancelled the dialog.';
        });
  };

  $scope.showPrerenderedDialog = function(ev) {
    $mdDialog.show({
      contentElement: '#myDialog',
      parent: angular.element(document.body),
      targetEvent: ev,
      clickOutsideToClose: true
    });
  };

  function DialogController($scope, $mdDialog) {
    $scope.hide = function() {
      $mdDialog.hide();
    };

    $scope.cancel = function() {
      $mdDialog.cancel();
    };

    $scope.answer = function(answer) {
      $mdDialog.hide(answer);
    };
  }
});

//mainController holds the icons and links of outsourced projects
app.controller('mainController', function($scope) {
    $scope.message = "hello world";
});

//change title according to page landing
app.run(['$rootScope', function($rootScope) {
    $rootScope.$on('$routeChangeSuccess', function(event, current, previous) {
        $rootScope.title = current.$$route.title;
        // $rootScope.selected = current.$$route.selected;
        // $rootScope.selected1 = current.$$route.selected1;
        // $rootScope.selected2 = current.$$route.selected2;
    });
}]);

function submitTrip(){
        $.ajax({
                 type:"POST",
                 url:"/api/requestAjax/",
                 data: JSON.stringify({"req":0}),
                 success: function(result){
                     alert('SUCCESS!\n' + JSON.stringify(result));
                     location.reload();
                 }
                });
      }