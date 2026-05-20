(function ( $ ) {
    $.fn.numberfy = function(options){
        var _obj = this;

        var settings = $.extend({
            allow_negative: true,
            allow_decimal: true,
            allow_utilities: true,
            allow_exponent: false,
            comma_formatted: false,
            min: _obj.is("[min]") ? _obj.attr("min") : false,
            max: _obj.is("[max]") ? _obj.attr("max") : false,
        }, options );


        var allow_negative  = settings.allow_negative;
        var allow_decimal   = settings.allow_decimal;
        var allow_exponent  = settings.allow_exponent;
        var allow_utilities = settings.allow_utilities;
        var comma_formatted = settings.comma_formatted;

        _obj.keydown(function (e) { 
            _this = $(this);
            input_val = _this.val();

            // Allow: backspace, delete, tab, escape, enter and...
            if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110]) !== -1 ||
            // Allow: Ctrl/cmd+V
            (e.keyCode == 86 && (e.ctrlKey === true || e.metaKey === true) && allow_utilities) ||
                 // Allow: Ctrl/cmd+A
                (e.keyCode == 65 && (e.ctrlKey === true || e.metaKey === true) && allow_utilities) ||
                 // Allow: Ctrl/cmd+C
                (e.keyCode == 67 && (e.ctrlKey === true || e.metaKey === true) && allow_utilities) ||
                 // Allow: Ctrl/cmd+X
                (e.keyCode == 88 && (e.ctrlKey === true || e.metaKey === true) && allow_utilities) ||
                 // Allow: Ctrl/cmd+Z
                (e.keyCode == 90 && (e.ctrlKey === true || e.metaKey === true) && allow_utilities) ||
                 // Allow: negative
                (e.keyCode == 189 && allow_negative && input_val.length < 1) ||
                 // Allow: dot only once
                ((e.key == "." && input_val.indexOf(".") == -1) && allow_decimal) ||
                 // Allow: exponential
                (e.keyCode == 69 && allow_exponent) ||
                 // Allow: home, end, left, right
                (e.keyCode >= 35 && e.keyCode <= 39)
            ){
                // Add zero if first character input is a dot
                if(e.key == "." && input_val.length < 1)
                    _this.val("0");

                return;
            }

            // Ensure that it is a number and stop the keypress
            if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
                e.preventDefault();
            }
        });
 

        if(comma_formatted)
        {
            _obj.on("input", function(e){
                _this       = $(this);
                input_val   =  _this.val();
                values      = input_val.split(".");
                whole_num   = values[0];
                decimal_num = values.length > 1 ? '.' + values[1] : '';

                value = whole_num
                    .replace(/\D/g, "")
                    .replace(/\B(?=(\d{3})+(?!\d))/g, ",");

                _this.val(value+decimal_num);
            });
        }
    };
}(jQuery));