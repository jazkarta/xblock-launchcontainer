function getURLOrigin(path) {
    var link = document.createElement('a');
    link.setAttribute('href', path);

    port = (link.port) ? ':'+link.port : '';
    return link.protocol + '//' + link.hostname + port;
}

function LaunchContainerXBlock(runtime, element) {

    $(document).ready(
      function () {
        var $launcher = $('#launcher1'), $launch_button = $launcher.find('input');
        $launch_button.click(function() {
            console.log('Clicked launch button');
            $launch_button.attr('disabled', 'disabled').val('Launching...');
            $launcher.find('iframe')[0].contentWindow.postMessage({
                owner_email: "{{ user_email }}",
                project: "{{ project }}"
            }, "{{ API_url }}");
            return false;
        });
        window.addEventListener("message", function (event) {
            if (event.origin !== getURLOrigin('{{ API_url }}')) return;
            if(event.data.status === 'siteDeployed') {
                $launcher.html(event.data.html_content);
            } else if(event.data.status === 'deploymentError') {
                $launcher.text(event.data.error_message);
            }
        }, false);
    });

}
