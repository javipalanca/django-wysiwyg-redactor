if (typeof jQuery === 'undefined' && django && django.jQuery) {
    jQuery = django.jQuery;
}

if (typeof custom_options === 'undefined') {
    custom_options = {}
}

(function($) {
    $(document).ready(function() {
        $(document).on('redactor:init', 'textarea.redactor-box', function() {
            var options = $.extend({}, $(this).data('redactor-options'), custom_options);
            if (typeof options.callbacks === 'undefined') {
                options.callbacks = {};
            }
            if (typeof options.callbacks.imageUploadError === 'undefined') {
                options.callbacks.imageUploadError = function (json, xhr) {
                    if (json.error) {
                        if (json.message) {
                            alert(json.message);
                        } else {
                            alert('Something went wrong!');
                        }
                    }
                }
            }
            $(this).redactor(options);
        });

        $('textarea.redactor-box:not([id*="__prefix__"])').each(function() {
            $(this).trigger('redactor:init');
        });

        // Initialize Redactor on admin's dynamically-added inline
        // formsets.
        //
        // Credit to the approach taken in django-selectable:
        // https://github.com/mlavin/django-selectable
        $(document).on('click', '.add-row', function () {
            var add_row = $(this);
            var row = add_row.parents('.inline-related')
                      .find('tr.form-row:not(.empty-form)').last();
            if (row.length === 0) {
                row = add_row.parents('.inline-group')
                      .find('.last-related:not(.empty-form)').last();
            }
            row.find('textarea.redactor-box').trigger('redactor:init');
        });
    });
})(jQuery);
