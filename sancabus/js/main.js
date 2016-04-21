var app = angular.module('myApp', []);

app.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/linhas', {
        templateUrl: 'lista.html',
        controller: 'LinhasController'
      }).
      when('/linha/:numero', {
        templateUrl: 'linha.html',
        controller: 'LinhaController'
      }).
      otherwise({
        redirectTo: '/linhas'
      });
  }]);

app.run(function ($rootScope, $location) {

    var history = [];

    $rootScope.$on('$routeChangeSuccess', function() {
        history.push($location.$$path);
    });

    $rootScope.back = function () {
        var prevUrl = history.length > 1 ? history.splice(-2)[0] : "/";
        $location.path(prevUrl);
    };

});

app.controller("LinhasController", function($scope, $http) {

  $scope.input = {};

  $scope.removerAcentos = function(val) {
    var mapaAcentosHex 	= { // by @marioluan and @lelotnk
    	a : /[\xE0-\xE6]/g,
    	A : /[\xC0-\xC6]/g,
    	e : /[\xE8-\xEB]/g, // if you're gonna echo this
    	E : /[\xC8-\xCB]/g, // JS code through PHP, do
    	i : /[\xEC-\xEF]/g, // not forget to escape these
    	I : /[\xCC-\xCF]/g, // backslashes (\), by repeating
    	o : /[\xF2-\xF6]/g, // them (\\)
    	O : /[\xD2-\xD6]/g,
    	u : /[\xF9-\xFC]/g,
    	U : /[\xD9-\xDC]/g,
    	c : /\xE7/g,
    	C : /\xC7/g,
    	n : /\xF1/g,
    	N : /\xD1/g,
    };

    for ( var letra in mapaAcentosHex ) {
    	var expressaoRegular = mapaAcentosHex[letra];
    	val = val.replace( expressaoRegular, letra );
    }

    val = val.toLowerCase();
    val = val.replace(/[^a-z0-9\-]/g, " ");

    val = val.replace(/ {2,}/g, " ");

    val = val.trim();

    return val;
  };

  $scope.busca = function() {

    var localSaida = $scope.input.saida;
    var localChegada = $scope.input.chegada;

    if ((typeof localSaida === "undefined") || (localSaida == "")) {
      localSaida = "all";
    }

    if ((typeof localChegada === "undefined") || (localChegada == "")) {
      localChegada = "all";
    }

    localSaida = $scope.removerAcentos(localSaida);
    localChegada = $scope.removerAcentos(localChegada);

    $http.get('http://localhost:4567/linhas/' + localSaida + "/" + localChegada).
      success(function(data, status, headers, config) {
        $scope.linhas = data;

        if (data == "") {
          alert("Não foram encontradas rotas entre os endereços.");
        }
      }).
      error(function(data, status, headers, config) {
        console.log("Erro ao obter dados da rota");
      });
  };
});

app.controller("LinhaController", function($scope, $http, $routeParams) {

  $http.get('http://localhost:4567/linha/' + $routeParams.numero).
    success(function(data, status, headers, config) {

      $scope.linha = data;

    }).
    error(function(data, status, headers, config) {
      console.log("Erro ao obter dados da rota");
    });
});
