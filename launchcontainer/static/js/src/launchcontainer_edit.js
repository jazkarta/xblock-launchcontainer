function LaunchContainerEditBlock(runtime, element) {
    console.log($('.xblock-save-button', element));
    $('.save-button', element).bind('click', function() {
        var handlerUrl = runtime.handlerUrl(element, 'studio_submit');
        var data = {
            'project': $('input[name=project]').val(),
            'project_friendly': $('input[name=project_friendly]').val(),
            'redir_url': $('input[name=redir_url]').val(),
        };
        runtime.notify('save', {state: 'start'});
        $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
            if (response.result === 'success') {
                runtime.notify('save', {state: 'end'});
            }
            else {
                runtime.notify('error', {msg: response.result});
                //$('#error-message', element).html('Error: '+response.result);
            }
        });
    });

    $('.cancel-button', element).bind('click', function() {
        runtime.notify('cancel', {});
    });
}

