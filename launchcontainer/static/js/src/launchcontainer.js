$(document).ready(
  function () {
    var $launcher = $('#launcher1'), $launch_button = $launcher.find('input');
    $launch_button.click(function() {
        console.log('Clicked launch button');
        $launch_button.attr('disabled', 'disabled').val('Launching...');
        $launcher.find('iframe')[0].contentWindow.postMessage({
            owner_email: "{{ user_email }}",
            project: "{{ project }}"
        }, "https://isc.appsembler.com");
        return false;
    });
    window.addEventListener("message", function (event) {
        if (event.origin !== 'https://isc.appsembler.com') return;
        if(event.data.status === 'siteDeployed') {
            $launcher.html(event.data.html_content);
        } else if(event.data.status === 'deploymentError') {
            $launcher.text(event.data.error_message);
        }
    }, false);
});

