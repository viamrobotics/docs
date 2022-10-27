(function($) {

    'use strict';

    var Search = {
        init: function() {
            $(document).ready(function() {
               $(document).on('keypress', '.navbar-nav .td-search-input', function(e) {
                    if (e.keyCode === 13) {
                        e.preventDefault();
                        return;
                    }
                });
               $(document).on('keypress', '.td-sidebar__search .td-search-input', function(e) {
                    if (e.keyCode === 13) {
                        e.preventDefault();
                        return;
                    }
                });
            });
        },
    };

    Search.init();

}(jQuery));