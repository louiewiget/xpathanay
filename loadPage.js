var page = require('webpage').create(),
      system = require('system'),
        address;
if (system.args.length === 1) {
      phantom.exit(1);
} else {
      address = system.args[1];
      page.onConsoleMessage = function(msg) {
              console.log(msg);
      };
      page.settings.userAgent='Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
        page.open(address, function (status) {
            //console.log(page.content);
            //phantom.exit(0);
            window.setTimeout(function() {
                console.log(page.content);
                phantom.exit();
            }, 3000);
        });
}
