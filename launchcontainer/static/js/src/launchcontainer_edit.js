function LaunchContainerEditBlock(runtime, element) {
    console.log($('.xblock-save-button', element));
    $('.action-save', element).bind('click', function() {
        var data = {
            'project': $('#project_input').val(),
        };
        var handlerUrl = runtime.handlerUrl(element, 'studio_submit');
        $.post(handlerUrl, JSON.stringify(data)).complete(function() {
            if (response.result === 'success') {
                window.location.reload(false);
            } else {
                $('.error-message', element).html('Error: '+response.message);
            }            
        });
    });

    $('.action-cancel', element).bind('click', function() {
        runtime.notify('cancel', {});
    });
}

